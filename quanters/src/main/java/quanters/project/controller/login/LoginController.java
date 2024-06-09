package quanters.project.controller.login;

import lombok.RequiredArgsConstructor;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;
import java.sql.Timestamp;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

import quanters.project.dto.login.PrincipalDetails;
import quanters.project.entity.login.UserEntity;
import quanters.project.entity.stock.StockEntity;
import quanters.project.repository.login.UserRepository;
import quanters.project.repository.stock.StockRepository;
import quanters.project.service.login.LoginService;

@Controller // ResponseBody 필요없음
@RequiredArgsConstructor // final 객체를 Constructor Injection 해줌. Autowired 필요없음
@RequestMapping("/login")
public class LoginController {
    Logger logger = LoggerFactory.getLogger(this.getClass());

    private final UserRepository userRepository;
    private final StockRepository stockRepository;
    private final LoginService loginService;

    @GetMapping("/loginPage")
    public String goLoginPage(HttpServletRequest request, HttpServletResponse response, Model model) {
        String errorCode = request.getParameter("error");
        String errorMessage;

        if(errorCode != null) {
            if(errorCode.equals("1")) {
                errorMessage = "계정이 존재하지 않습니다.";
            } else if(errorCode.equals("2")) {
                errorMessage = "아이디 또는 비밀번호가 맞지 않습니다.";
            } else if(errorCode.equals("3")) {
                errorMessage = "내부적으로 발생한 시스템 문제로 인해 요청을 처리할 수 없습니다. 관리자에게 문의하세요.";
            } else if(errorCode.equals("4")) {
                errorMessage = "인증 요청이 거부되었습니다. 관리자에게 문의하세요.";
            } else if(errorCode.equals("5")) {
                errorMessage = "잠겨있는 계정입니다. 관리자에게 문의하세요.";
            } else if(errorCode.equals("6")) {
                errorMessage = "만료된 계정입니다.";
            } else if(errorCode.equals("7")) {
                errorMessage = "인증 요청이 거부되었습니다. 관리자에게 문의하세요.";
            } else {
                errorMessage = "알 수 없는 이유로 로그인에 실패하였습니다 관리자에게 문의하세요.";
            }
            logger.info(errorMessage);
            model.addAttribute("errorMessage", errorMessage);
        }
        return "login/loginPage";
    }

    @GetMapping("/myPage")
    public String goMyPage(HttpServletRequest request, Model model) {
        HttpSession session = request.getSession(true);
        Object principal = session.getAttribute("sessionUser");
        if(principal instanceof PrincipalDetails) {
            PrincipalDetails userDetails = (PrincipalDetails) principal;
            String userId = userDetails.getUsername();
            String authorities = userDetails.getAuthorities().toString();
            model.addAttribute("userId", userId);
        }
        return "login/myPage";
    }
    @GetMapping("/registerPage")
    public String goRegisterPage(HttpServletRequest request, Model model) {
        HttpSession session = request.getSession(true);
        Object principal = session.getAttribute("sessionUser");
        if(principal instanceof PrincipalDetails) {
            PrincipalDetails userDetails = (PrincipalDetails) principal;
            String userId = userDetails.getUsername();
            String authorities = userDetails.getAuthorities().toString();
            model.addAttribute("userId", userId);
        }
        return "login/registerPage";
    }

    @ResponseBody
    @PostMapping(value = "/register", produces = "application/json;charset=utf-8")
    public int register (@RequestBody Map<String, Object> param, HttpServletRequest request) throws Throwable {
        try {
            String userId = (String) param.get("userId");
            BCryptPasswordEncoder encoder = new BCryptPasswordEncoder();
            String userPw = encoder.encode((String) param.get("userPw"));
            String userState = (String) param.get("userState");
            Timestamp now = new Timestamp(System.currentTimeMillis());
            UserEntity user = UserEntity.builder().userId(userId).userPw(userPw).createDate(now).userState(userState).build();
            userRepository.save(user);
            return 1;
        } catch (Exception e) {
            logger.info("Error");
            return 0;
        }
    }

}
