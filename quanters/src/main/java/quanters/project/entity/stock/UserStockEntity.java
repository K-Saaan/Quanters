package quanters.project.entity.stock;

import lombok.*;

import javax.persistence.*;
import java.util.UUID;

@Getter
@Entity
@Builder
@AllArgsConstructor
@NoArgsConstructor(access = AccessLevel.PROTECTED)
@Table(name = "user_stock_info")
public class UserStockEntity {
    @Id
    @GeneratedValue
    @Column(name = "id")
    private UUID id;
    @Column(name = "user_id")
    private String userId;
    @Column(name = "stock_name")
    private String stockName;
}
