package quanters.project.service.login;

import javax.servlet.http.HttpServletRequest;
import java.util.Map;

public interface LoginService {
    public Map<String, Object> updateLogin(String id, String pwd, HttpServletRequest request);
}
