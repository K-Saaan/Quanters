package quanters.project.controller.home;

import com.opencsv.CSVReader;

import java.io.FileReader;
import java.io.IOException;
import java.nio.charset.Charset;

public class CsvParser {
    public void csvParser() throws Exception {
        try {
            CSVReader reader = new CSVReader(new FileReader("/Users/kdh/Documents/csv/test3.csv", Charset.forName("utf-8")));
            String[] nextline;
            while((nextline = reader.readNext()) != null) {
                if (nextline != null) {
                    System.out.println(nextline[0] + nextline[1] + nextline[2]);
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
