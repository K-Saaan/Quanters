package quanters.project.service.aws;

import com.amazonaws.services.s3.AmazonS3;
import com.amazonaws.services.s3.model.GetObjectRequest;
import com.amazonaws.services.s3.model.S3Object;
import com.amazonaws.services.s3.model.S3ObjectInputStream;
import com.amazonaws.util.IOUtils;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.URLEncoder;

@Service
@Transactional(readOnly = true)
@RequiredArgsConstructor
public class S3Service {
    private final AmazonS3 amazonS3;

    @Value("${cloud.aws.s3.bucket}")
    private String bucket;

    public void getObject(String storedFileName) throws IOException {
        S3Object o = amazonS3.getObject(new GetObjectRequest(bucket, storedFileName));
        S3ObjectInputStream objectInputStream = ((S3Object) o).getObjectContent();

        // S3 bucket 파일 다운로드 ResponseEntity<byte[]> -> void
//        byte[] bytes = IOUtils.toByteArray(objectInputStream);
//        String fileName = URLEncoder.encode(storedFileName, "UTF-8").replaceAll("\\+", "%20");
//        HttpHeaders httpHeaders = new HttpHeaders();
//        httpHeaders.setContentType(MediaType.APPLICATION_OCTET_STREAM);
//        httpHeaders.setContentLength(bytes.length);
//        httpHeaders.setContentDispositionFormData("attachment", fileName);
//
//        return new ResponseEntity<>(bytes, httpHeaders, HttpStatus.OK);

        BufferedReader br = null;
        br = new BufferedReader(new InputStreamReader(objectInputStream, "UTF-8"));
        String line;
        while ((line = br.readLine()) != null) {
            String[] data = line.split(",", 0);
            if (data != null) {
                System.out.println(data[0] + data[1] + data[2]);
            }
        }
    }
}
