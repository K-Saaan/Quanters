package quanters.project.entity.stock;

import lombok.*;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.Table;

@Getter
@Entity
@Builder
@AllArgsConstructor
@NoArgsConstructor(access = AccessLevel.PROTECTED)
@Table(name = "stock_info")
public class StockEntity {
    @Id
    @Column(name = "stock_code")
    private String stockCode;
    @Column(name = "stock_name")
    private String stockName;
}
