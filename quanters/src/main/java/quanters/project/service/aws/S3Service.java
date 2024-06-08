package quanters.project.service.aws;

import com.amazonaws.AmazonServiceException;
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
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.URLEncoder;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@Service
@Transactional(readOnly = true)
@RequiredArgsConstructor
public class S3Service {
    private final Logger logger = LoggerFactory.getLogger(getClass());
    private final AmazonS3 amazonS3;

    @Value("${cloud.aws.s3.bucket}")
    private String bucket;

    public String getObject(String storedFileName, String stockName) throws IOException {
        try {
            S3Object o = amazonS3.getObject(new GetObjectRequest(bucket, storedFileName));
            S3ObjectInputStream objectInputStream = ((S3Object) o).getObjectContent();

            String stockCode = "";
            if(stockName.equals("카카오")) {
                stockCode = "0";
            } else if(stockName.equals("네이버")) {
                stockCode = "2";
            } else if(stockName.equals("SK하이닉스")) {
                stockCode = "1";
            } else if(stockName.equals("삼성전자")) {
                stockCode = "3";
            }

            BufferedReader br = null;
            br = new BufferedReader(new InputStreamReader(objectInputStream, "UTF-8"));
            String line;
            String result = "";
            while ((line = br.readLine()) != null) {
                String[] data = line.split(",", 0);
                if (data != null) {
                    if(data[0].equals(stockCode)) {
                        if(data[6].equals("1")) {
                            result = "up";
                        } else {
                            result = "down";
                        }
                    }
                }
            }
            return result;
        } catch (AmazonServiceException e) {
            logger.info("AmazonServiceException");
            e.printStackTrace();
        } catch (FileNotFoundException e) {
            logger.info("FileNotFoundException");
            e.printStackTrace();
        } catch (IOException e) {
            logger.info("IOException");
            e.printStackTrace();
        }
        return "error";
    }
}
