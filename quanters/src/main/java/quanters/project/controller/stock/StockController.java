package quanters.project.controller.stock;

import lombok.RequiredArgsConstructor;
import org.apache.catalina.User;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import quanters.project.dto.login.PrincipalDetails;
import quanters.project.entity.stock.StockEntity;
import quanters.project.entity.stock.StockHistEntity;
import quanters.project.entity.stock.UserStockEntity;
import quanters.project.repository.stock.StockHistRepository;
import quanters.project.repository.stock.StockRepository;
import quanters.project.repository.stock.UserStockRepository;
import quanters.project.service.aws.S3Service;
import quanters.project.service.stock.StockService;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpSession;
import java.io.IOException;
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.*;
import java.util.stream.Collectors;

@Controller // ResponseBody 필요없음
@RequiredArgsConstructor // final 객체를 Constructor Injection 해줌. Autowired 필요없음
@RequestMapping("/stock")
public class StockController {
    Logger logger = LoggerFactory.getLogger(this.getClass());
    private final StockRepository stockRepository;
    private final UserStockRepository userStockRepository;
    private final StockHistRepository stockHistRepository;
    private final StockService stockService;
    private final S3Service s3Service;

    @ResponseBody
    @PostMapping(value = "/showAllStock", produces = "application/json;charset=utf-8")
    public Map<String, Object> showAllStock (@RequestBody Map<String, Object> param, HttpServletRequest request) throws Throwable {
        HttpSession session = request.getSession(true);
        Map<String, Object> result = new HashMap();
        Object principal = session.getAttribute("sessionUser");
        if(principal instanceof PrincipalDetails) {
            PrincipalDetails userDetails = (PrincipalDetails) principal;
            String userId = userDetails.getUsername();
            List<StockEntity> stockList = stockRepository.findAll();
            result.put("stockList", stockList);
        }
        return result;
    }
    @ResponseBody
    @PostMapping(value = "/insertUserStock", produces = "application/json;charset=utf-8")
    public int insertUserStock (@RequestBody Map<String, Object> param, HttpServletRequest request) throws Throwable {
        try {
            HttpSession session = request.getSession(true);
            Object principal = session.getAttribute("sessionUser");
            if(principal instanceof PrincipalDetails) {
                PrincipalDetails userDetails = (PrincipalDetails) principal;
                String userId = userDetails.getUsername();
                // 접속 사용자의 기존에 추가되어있는 주가 리스트 확인
                List<UserStockEntity> existStockList = userStockRepository.findByUserId(userId);
                String existStockCode = "";
                // 파라미터로 받아온 이번에 추가할 주가 리스트
                ArrayList<String> paramStockArr = (ArrayList<String>) param.get("stockCode");
                ArrayList<String> newArr = new ArrayList<String>();
                for(UserStockEntity existStock:existStockList) {
                    existStockCode = existStock.getStockCode();
                    newArr.add(existStockCode);
                }
                String addStockName = "";
                // 새로 추가할 주가 리스트 중에서 기존에 이미 있는 주가는 제외
                ArrayList<String> diffArr = (ArrayList<String>) paramStockArr.stream()
                        .filter(element -> !newArr.contains(element))
                        .collect(Collectors.toList());
                for (String paramStockCode:diffArr) {
                    List<StockEntity> stockNameList = stockRepository.findByStockCode(paramStockCode);
                    for(StockEntity stockName:stockNameList) {
                        addStockName = stockName.getStockName();
                    }
                    UserStockEntity userStock = UserStockEntity.builder().userId(userId).stockCode(paramStockCode).stockName(addStockName).build();
                    userStockRepository.save(userStock);
                }
                return 1;
            } else {
                return 0;
            }
        } catch (Exception e) {
            logger.info("Error");
            logger.error(String.valueOf(e));
            return 0;
        }
    }
    @ResponseBody
    @PostMapping(value = "/showUserStock", produces = "application/json;charset=utf-8")
    public Map<String, Object> showUserStock (@RequestBody Map<String, Object> param, HttpServletRequest request) throws Throwable {
        Map<String, Object> result = new HashMap();
        try {
            HttpSession session = request.getSession(true);
            Object principal = session.getAttribute("sessionUser");
            if(principal instanceof PrincipalDetails) {
                PrincipalDetails userDetails = (PrincipalDetails) principal;
                String userId = userDetails.getUsername();
                List<UserStockEntity> stockList = userStockRepository.findByUserId(userId);
                result.put("stockList", stockList);
            } else {
                result.put("stockList", "error");
            }
        } catch (Exception e) {
            logger.info("Error");
            logger.error(String.valueOf(e));
            result.put("stockList", "error");
        }
        return result;
    }

    @ResponseBody
    @PostMapping(value = "/deleteUserStock", produces = "application/json;charset=utf-8")
    public int deleteUserStock (@RequestBody Map<String, Object> param, HttpServletRequest request) throws Throwable {
        int resultNum = 0;
        try {
            HttpSession session = request.getSession(true);
            Object principal = session.getAttribute("sessionUser");
            if(principal instanceof PrincipalDetails) {
                PrincipalDetails userDetails = (PrincipalDetails) principal;
                String userId = userDetails.getUsername();
                // 파라미터로 받아온 이번에 추가할 주가 리스트
                ArrayList<String> paramStockArr = (ArrayList<String>) param.get("stockName");
                List<UUID> uuidArr = new ArrayList<>();
                for (String paramStockName:paramStockArr) {
                    List<UserStockEntity> existStockList = userStockRepository.findByUserIdAndStockName(userId, paramStockName);
                    for (UserStockEntity userStockEntity:existStockList) {
                        uuidArr.add(userStockEntity.getId());
                    }
                }
                resultNum = stockService.deleteUserStock(uuidArr);
                return resultNum;
            } else {
                return resultNum;
            }
        } catch (Exception e) {
            logger.info("Error");
            logger.error(String.valueOf(e));
            return resultNum;
        }
    }

    @ResponseBody
    @PostMapping(value = "/showStockHist", produces = "application/json;charset=utf-8")
    public Map<String, Object> showStockHist (@RequestBody Map<String, Object> param, HttpServletRequest request) throws Throwable {
        Map<String, Object> result = new HashMap();
        String stockCode = (String) param.get("stockCode");
        try {
            HttpSession session = request.getSession(true);
            Object principal = session.getAttribute("sessionUser");
            if(principal instanceof PrincipalDetails) {
                PrincipalDetails userDetails = (PrincipalDetails) principal;
                String userId = userDetails.getUsername();
                List<StockHistEntity> stockList = stockHistRepository.findByStockCodeOrderByStockDateDesc(stockCode);
                result.put("stockList", stockList);
            } else {
                result.put("stockList", "error");
            }
        } catch (Exception e) {
            logger.info("Error");
            logger.error(String.valueOf(e));
            result.put("stockList", "error");
        }
        return result;
    }

    @ResponseBody
    @PostMapping(value = "/showStockPredict", produces = "application/json;charset=utf-8")
    public Map<String, Object> showStockPredict(@RequestBody Map<String, Object> param, HttpServletRequest request) {
        Map<String, Object> result = new HashMap();
        String stockName = (String) param.get("stockName");
        HttpSession session = request.getSession(true);
        Object principal = session.getAttribute("sessionUser");
        if(principal instanceof PrincipalDetails) {
            PrincipalDetails userDetails = (PrincipalDetails) principal;
            String userId = userDetails.getUsername();
            String authorities = userDetails.getAuthorities().toString();
        }
        LocalDate now = LocalDate.now();
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyyMMdd");
        String formatedNow = now.format(formatter);
        String yyyyMM = formatedNow.substring(0,6);
        String dd = formatedNow.substring(6);
        String resultMsg = "";
        try {
            resultMsg = s3Service.getObject(yyyyMM + "/result_" + dd + ".csv", stockName);
        } catch (IOException e) {
            e.printStackTrace();
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
        result.put("resultMsg", resultMsg);
        return result;
    }
}
