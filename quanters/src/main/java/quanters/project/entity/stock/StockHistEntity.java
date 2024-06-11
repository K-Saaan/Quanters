package quanters.project.entity.stock;

import lombok.*;

import javax.persistence.*;
import java.util.UUID;

@Getter
@Entity
@Builder
@AllArgsConstructor
@NoArgsConstructor(access = AccessLevel.PROTECTED)
@Table(name = "stock_hist")
public class StockHistEntity {
    @Id
    @GeneratedValue
    @Column(name = "id")
    private int id;
    @Column(name = "stock_code")
    private String stockCode;
    @Column(name = "stock_name")
    private String stockName;
    @Column(name = "stock_date")
    private String stockDate;
    @Column(name = "open_price")
    private int openPrice;
    @Column(name = "high_price")
    private int highPrice;
    @Column(name = "low_price")
    private int lowPrice;
    @Column(name = "close_price")
    private int closePrice;
    @Column(name = "stock_volume")
    private int stockVolume;
    @Column(name = "stock_change")
    private float stockChange;
}
