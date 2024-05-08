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

            // 메인으로 이동
            resultMap.put("RESULT", "GO_MAIN");
//            resultMap.put("URL", user.getMainUrl());

            // 로그인 시간 update / 로그인 실패 횟수 0으로 초기화
//            mng.LoginUpdate(0, "N", id, today);
//            mngRepository.save(mng);
//
//            String stringToday = DateUtil.getStringToday();
//
//            // 로그인 이력 기록
//            LoginHistEntity loginHistEntity = LoginHistEntity.builder().mngId(id).loginDate(stringToday).regId(mng.getRegId())
//                    .regDate(mng.getRegDate()).chgrId(mng.getChgrId()).chgrDate(dateTime).build();

//            loginHsitRepository.save(loginHistEntity);

        }else {
            logger.info("login fail >>>>>>>");
            resultMap.put("RESULT", "LOGIN_FAIL");
            resultMap.put("URL", "");
//            MngEntity idCheck = mngRepository.findByMngId(id);
//            String dateTime = LocalDateTime.now().toString();
//            if(idCheck != null) {
//                int failCnt = idCheck.getLoginFailCnt();
//
//                if(failCnt >= 5) {
//                    resultMap.put("RESULT", "OVER_LOGIN_FAIL_CNT");
//                    resultMap.put("URL", "");
//                    idCheck.LoginUpdate(failCnt+1, "Y", id, dateTime);
//                    mngRepository.save(idCheck);
//                }else {
//                    resultMap.put("RESULT", "PWD_FAIL");
//                    resultMap.put("URL", "");
//                    resultMap.put("FAILCNT", failCnt+1);
//                    idCheck.LoginUpdate(failCnt+1, "N", id, dateTime);
//                    mngRepository.save(idCheck);
//                }
//            }else {
//                // 로그인 실패
//                resultMap.put("RESULT", "LOGIN_FAIL");
//                resultMap.put("URL", "");
//            }
        }
        HttpSession session = request.getSession(true);
        session.removeAttribute("userId");
        session.setAttribute("userId", id);

        return resultMap;
    }
}
