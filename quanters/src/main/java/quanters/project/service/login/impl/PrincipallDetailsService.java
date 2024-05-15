package quanters.project.service.login.impl;

import lombok.RequiredArgsConstructor;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;
import quanters.project.dto.login.PrincipalDetails;
import quanters.project.entity.login.UserEntity;
import quanters.project.repository.login.UserRepository;

@Service
@RequiredArgsConstructor
public class PrincipallDetailsService implements UserDetailsService {
    private  final Logger logger = LoggerFactory.getLogger(this.getClass());
    private final UserRepository userRepository;

    @Override
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
        UserEntity user = userRepository.findById(username).orElseThrow(() -> {
            return new UsernameNotFoundException("해당 유저를 찾을 수 없습니다.");
        });
        return new PrincipalDetails(user);
//        if(user != null) {
//            return new PrincipalDetails(user);
//        }
//        return null;
    }
}
