package quanters.project.controller.home;

import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.jpa.domain.Specification;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import quanters.project.entity.HomeEntity;
import quanters.project.repository.HomeRepository;
import quanters.project.service.aws.S3Service;
import quanters.project.service.home.HomeService;

import java.time.LocalDate;
import java.time.format.DateTimeFormatter;

import java.io.IOException;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpSession;

@Controller // ResponseBody 필요없음
@RequiredArgsConstructor // final 객체를 Constructor Injection 해줌. Autowired 필요없음
@RequestMapping("/home")
public class HomeController {
    Logger logger = LoggerFactory.getLogger(this.getClass());

    private final S3Service s3Service;
    private final HomeRepository homeRepository;
    private final HomeService homeService;

    @GetMapping("/search")
    public String showTestPage(HttpServletRequest request, Model model) {
        HttpSession session = request.getSession(true);
        String userId = (String) session.getAttribute("userId");
        if (userId != null) {
            model.addAttribute("userId", userId);
            logger.info("userId &&&&&&&&&&&&&&&&&&&");
            logger.info(userId);
        }
        return "home/search";
    }

    @GetMapping("/detail")
    public String searchDetail(@RequestParam(value = "keyword") String keyword, Model model) {
        model.addAttribute("keyword", keyword);
        LocalDate now = LocalDate.now();
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyyMMdd");
        String formatedNow = now.format(formatter);
        String yyyyMM = formatedNow.substring(0,6);
        String dd = formatedNow.substring(6);
        String result = "";

//        Specification<HomeEntity> spec = ((root, query, criteriaBuilder) -> null);
//        Map<String, Object> test = new HashMap();
//        String testName = "brokurly";
//        spec = spec.and(homeService.getByTestName(testName));
//        int pagingIndex = 0;
//        int pagingRows = 50;
//        PageRequest page = PageRequest.of(pagingIndex, pagingRows);
//        Page<HomeEntity> specHome = homeRepository.findAll(spec, page);
//        test.put("codeList", specHome);
//        logger.info("TEST%%%%%%%%%%%%%%%%%");
//        for(HomeEntity home : specHome) {
//            System.out.println( home.getTestName() );
//        }

        try {
            result = s3Service.getObject(yyyyMM + "/result_" + dd + ".csv", keyword);
            model.addAttribute("result", result);
        } catch (IOException e) {
            e.printStackTrace();
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
        return "home/detail";
    }
}
