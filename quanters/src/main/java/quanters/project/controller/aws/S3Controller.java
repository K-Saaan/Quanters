package quanters.project.controller.aws;

import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import quanters.project.service.aws.S3Service;

import java.io.IOException;

@Controller
@RequiredArgsConstructor
public class S3Controller {
    private final S3Service s3Service;

    // ResponseEntity<byte[]> -> void
//    @GetMapping("/csv_download/{fileName}")
//    public void download(@PathVariable String fileName) throws IOException {
//        s3Service.getObject(fileName);
//    }
}
