package quanters.project.repository.stock;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.JpaSpecificationExecutor;
import quanters.project.entity.stock.UserStockEntity;

import java.util.List;
import java.util.UUID;

public interface UserStockRepository extends JpaRepository<UserStockEntity, UUID>, JpaSpecificationExecutor<UserStockEntity> {
    List<UserStockEntity> findByUserId(String userId);
    List<UserStockEntity> findByUserIdAndStockName(String userId, String stockName);
}
