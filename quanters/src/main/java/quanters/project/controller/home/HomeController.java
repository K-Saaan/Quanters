package quanters.project.controller.home;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;

import java.io.IOException;

@Controller // ResponseBody 필요없음
@RequiredArgsConstructor // final 객체를 Constructor Injection 해줌. Autowired 필요없음
@RequestMapping("/home")
public class HomeController {
    @GetMapping("/search")
    public String showTestPage() {
        return "home/search";
    }

    @GetMapping("/detail")
    public String searchDetail(@RequestParam(value = "keyword") String keyword, Model model) {
        model.addAttribute("keyword", keyword);
        try {
            CsvParser csvParser = new CsvParser();
            csvParser.csvParser();
        } catch (IOException e) {
            e.printStackTrace();
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
        return "home/detail";
    }
}
