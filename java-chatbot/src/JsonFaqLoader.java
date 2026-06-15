import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;

import org.json.JSONArray;
import org.json.JSONObject;

public class JsonFaqLoader {
    public static class FaqEntry {
        public final String question;
        public final String answer;
        public FaqEntry(String question, String answer) {
            this.question = question;
            this.answer = answer;
        }
    }

    public static List<FaqEntry> loadFaq(Path faqJsonPath) throws IOException {
        String raw = Files.readString(faqJsonPath, StandardCharsets.UTF_8);
        JSONArray arr = new JSONArray(raw);

        List<FaqEntry> out = new ArrayList<>();
        for (int i = 0; i < arr.length(); i++) {
            JSONObject obj = arr.getJSONObject(i);
            String q = obj.getString("question");
            String a = obj.getString("answer");
            out.add(new FaqEntry(q, a));
        }
        return out;
    }
}

