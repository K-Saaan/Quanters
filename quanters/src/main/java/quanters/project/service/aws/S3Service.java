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

    public String getObject(String storedFileName, String stockName) throws IOException {
        S3Object o = amazonS3.getObject(new GetObjectRequest(bucket, storedFileName));
        S3ObjectInputStream objectInputStream = ((S3Object) o).getObjectContent();

        BufferedReader br = null;
        br = new BufferedReader(new InputStreamReader(objectInputStream, "UTF-8"));
        String line;
        String result = "";
        while ((line = br.readLine()) != null) {
            String[] data = line.split(",", 0);
            if (data != null) {
                if(data[0].equals(stockName)) {
                    if(data[1].equals("up")) {
                        result = "up";
                    } else {
                        result = "down";
                    }
                }
            }
        }
        return result;
    }
}
