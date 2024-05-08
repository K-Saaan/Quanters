package quanters.project.controller.login;

import lombok.RequiredArgsConstructor;
import org.apache.catalina.User;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import quanters.project.common.AES256Util;

import javax.crypto.BadPaddingException;
import javax.crypto.IllegalBlockSizeException;
import javax.crypto.NoSuchPaddingException;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;
import java.io.UnsupportedEncodingException;
import java.security.InvalidAlgorithmParameterException;
import java.security.InvalidKeyException;
import java.security.NoSuchAlgorithmException;
import java.sql.Timestamp;
import java.util.Map;
import org.springframework.beans.factory.annotation.Value;
import quanters.project.entity.login.UserEntity;
import quanters.project.repository.login.UserRepository;
import quanters.project.service.login.LoginService;

@Controller // ResponseBody 필요없음
@RequiredArgsConstructor // final 객체를 Constructor Injection 해줌. Autowired 필요없음
@RequestMapping("/login")
public class LoginController {
    Logger logger = LoggerFactory.getLogger(this.getClass());

    @Value("${key.aesKey}")
    private String key;

    private final UserRepository userRepository;
    private final LoginService loginService;

    @GetMapping("/loginPage")
    public String goLoginPage() {
        return "login/loginPage";
    }

    @GetMapping("/logout")
    public String logout(HttpServletRequest request, Model model) {
        HttpSession session = request.getSession(false);
        if(session != null) {
            session.invalidate();
        }
        return "home/search";
    }

    @GetMapping("/myPage")
    public String goMyPage() {
        return "login/myPage";
    }
    @GetMapping("/registerPage")
    public String goRegisterPage() {
        return "login/registerPage";
    }

    @ResponseBody
    @PostMapping(value = "/loginAction", produces = "application/json;charset=utf-8")
    public Object loginAction(@RequestBody Map<String, Object> param,
                              Model model,
                              HttpServletRequest request,
                              HttpServletResponse response) throws InvalidKeyException, UnsupportedEncodingException, NoSuchAlgorithmException, NoSuchPaddingException, InvalidAlgorithmParameterException, IllegalBlockSizeException, BadPaddingException {

        String id = (String) param.get("text_id");
        String pwd = (String) param.get("text_pwd");
//        pwd = AES256Util.enCode(pwd, key);
        return loginService.updateLogin(id, pwd, request);
    }

    @ResponseBody
    @PostMapping(value = "/register", produces = "application/json;charset=utf-8")
    public int register (@RequestBody Map<String, Object> param, HttpServletRequest request) throws Throwable {
        try {
            String userId = (String) param.get("userId");
            String userPw = (String) param.get("userPw");
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
