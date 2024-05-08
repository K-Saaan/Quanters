package quanters.project.service.home.impl;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.jpa.domain.Specification;
import org.springframework.stereotype.Service;
import quanters.project.entity.HomeEntity;
import quanters.project.repository.HomeRepository;
import quanters.project.service.home.HomeService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@Service
public class HomeServiceImpl implements HomeService {
    private final Logger logger = LoggerFactory.getLogger(this.getClass());

    @Autowired
    private HomeRepository homeRepository;

    @Override
    public Specification<HomeEntity> getByTestName(String testName) {
        return (root, query, criteriaBuilder) -> criteriaBuilder.like(root.get("testName"), "%" + testName + "%");
    }
}
