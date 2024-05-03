package quanters.project.repository.login;

import org.apache.catalina.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.JpaSpecificationExecutor;
import quanters.project.entity.login.UserEntity;
import org.springframework.data.repository.query.Param;
import org.springframework.data.jpa.repository.Query;

public interface UserRepository extends JpaRepository<UserEntity, String>, JpaSpecificationExecutor<UserEntity> {
    UserEntity findByUserId(String userId);

    UserEntity findByUserIdAndUserPw(String userId, String userPw);

    @Query(value = "select * from user_info where USER_ID = :userId and USER_PW = :userPw", nativeQuery=true)
    UserEntity findByUser(@Param("userId") String userId, @Param("userPw") String userPw);
}
