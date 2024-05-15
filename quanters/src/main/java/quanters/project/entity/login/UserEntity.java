package quanters.project.entity.login;

import lombok.*;

import javax.persistence.*;
import java.sql.Timestamp;

@Getter
@Entity
@Builder
@AllArgsConstructor
@NoArgsConstructor(access = AccessLevel.PROTECTED)
@Table(name = "user_info")
public class UserEntity {
    @Id
    @Column(name = "user_id")
    private String userId;
    @Column(name = "user_pw")
    private String userPw;
    @Column(name = "create_date")
    private Timestamp createDate;
    @Column(name = "user_state")
    private String userState;
    @Column(name = "role")
    private String role;
}
