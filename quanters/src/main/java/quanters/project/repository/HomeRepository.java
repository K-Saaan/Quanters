package quanters.project.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.JpaSpecificationExecutor;
import quanters.project.entity.HomeEntity;

import java.util.List;

public interface HomeRepository extends JpaRepository<HomeEntity, Integer>, JpaSpecificationExecutor<HomeEntity> {
    List<HomeEntity> findByTestName(String testName);
}
