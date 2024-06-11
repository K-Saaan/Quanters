package quanters.project.repository.stock;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.JpaSpecificationExecutor;
import quanters.project.entity.stock.StockEntity;

import java.util.List;

public interface StockRepository extends JpaRepository<StockEntity, String>, JpaSpecificationExecutor<StockEntity> {
    List<StockEntity> findByStockCode(String stockCode);
}
