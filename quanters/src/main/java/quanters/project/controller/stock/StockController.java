package quanters.project.controller.stock;

import lombok.RequiredArgsConstructor;
import org.apache.catalina.User;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;
import quanters.project.dto.login.PrincipalDetails;
import quanters.project.entity.stock.StockEntity;
import quanters.project.entity.stock.UserStockEntity;
import quanters.project.repository.stock.StockRepository;
import quanters.project.repository.stock.UserStockRepository;
import quanters.project.service.stock.StockService;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpSession;
import java.util.*;
import java.util.stream.Collectors;

@Controller // ResponseBody 필요없음
@RequiredArgsConstructor // final 객체를 Constructor Injection 해줌. Autowired 필요없음
@RequestMapping("/stock")
public class StockController {
    Logger logger = LoggerFactory.getLogger(this.getClass());
    private final StockRepository stockRepository;
    private final UserStockRepository userStockRepository;
    private final StockService stockService;

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
                String existStockName = "";
                // 파라미터로 받아온 이번에 추가할 주가 리스트
                ArrayList<String> paramStockArr = (ArrayList<String>) param.get("stockName");
                ArrayList<String> newArr = new ArrayList<String>();
                for(UserStockEntity existStock:existStockList) {
                    existStockName = existStock.getStockName();
                    newArr.add(existStockName);
                }
                // 새로 추가할 주가 리스트 중에서 기존에 이미 있는 주가는 제외
                ArrayList<String> diffArr = (ArrayList<String>) paramStockArr.stream()
                        .filter(element -> !newArr.contains(element))
                        .collect(Collectors.toList());
                for (String paramStockName:diffArr) {
                    UserStockEntity userStock = UserStockEntity.builder().userId(userId).stockName(paramStockName).build();
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
}
