package quanters.project.service.stock.impl;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import quanters.project.repository.stock.UserStockRepository;
import quanters.project.service.stock.StockService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

@Service
@RequiredArgsConstructor // final 객체를 Constructor Injection 해줌. Autowired 필요없음
public class StockServiceImpl implements StockService {
    private  final Logger logger = LoggerFactory.getLogger(this.getClass());
    private final UserStockRepository userStockRepository;

    @Transactional
    public int deleteUserStock(List<UUID> uuidArr) {
        try {
            for (UUID id:uuidArr) {
                if (userStockRepository.findById(id).isPresent()) {
                    userStockRepository.deleteById(id);
                }
            }
            return 1;
        } catch (NullPointerException e) {
            logger.error("error", e);
            return 0;
        }
    }
}