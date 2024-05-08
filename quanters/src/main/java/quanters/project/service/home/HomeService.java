package quanters.project.service.home;

import org.springframework.data.jpa.domain.Specification;
import quanters.project.entity.HomeEntity;

public interface HomeService {
    Specification<HomeEntity> getByTestName(String testName);
}
