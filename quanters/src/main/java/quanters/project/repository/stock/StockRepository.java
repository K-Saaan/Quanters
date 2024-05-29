package quanters.project.repository.stock;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.JpaSpecificationExecutor;
import quanters.project.entity.stock.StockEntity;

public interface StockRepository extends JpaRepository<StockEntity, String>, JpaSpecificationExecutor<StockEntity> {

}
