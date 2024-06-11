package quanters.project.repository.stock;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.JpaSpecificationExecutor;
import quanters.project.entity.stock.StockHistEntity;

import java.util.List;

public interface StockHistRepository extends JpaRepository<StockHistEntity, Integer>, JpaSpecificationExecutor<StockHistEntity> {
    List<StockHistEntity> findByStockCodeOrderByStockDateDesc(String stockCode);
}
