package quanters.project.service.login.impl;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import quanters.project.entity.login.UserEntity;
import quanters.project.repository.login.UserRepository;
import quanters.project.service.login.LoginService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpSession;
import java.util.HashMap;
import java.util.Map;

@Service
public class LoginServiceImpl implements LoginService {
    private  final Logger logger = LoggerFactory.getLogger(this.getClass());

    @Autowired
    private UserRepository userRepository;

    @Override
    public Map<String, Object> updateLogin(String id, String pwd, HttpServletRequest request){

        Map<String,Object> resultMap= new HashMap<String, Object>();

        // Null 체크
        if ("".equals(id) || "".equals(pwd)) {
            resultMap.put("RESULT", "INPUT_NULL");
            resultMap.put("URL", "");
            return resultMap;
        }

        UserEntity user = userRepository.findByUserIdAndUserPw(id, pwd);

        logger.info("user :: " + user);
        if(user != null) {
            logger.info("login success >>>>>>>");
        }else {
            logger.info("login fail >>>>>>>");
        }
        HttpSession session = request.getSession(true);
        session.removeAttribute("userId");
        session.setAttribute("userId", id);

        return resultMap;
    }
}
