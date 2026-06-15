import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.Set;
import java.nio.file.Path;

import JsonFaqLoader.FaqEntry;

public class Chatbot {

    private final List<FaqEntry> faq;
    private final List<Set<String>> faqTokenSets;
    private final Map<String, Integer> faqTokenDocFreq;

    // Heuristics
    private final double minConfidence;

    public Chatbot(List<FaqEntry> faq) {
        this(faq, 0.18);
    }

    public Chatbot(List<FaqEntry> faq, double minConfidence) {
        this.faq = faq;
        this.minConfidence = minConfidence;
        this.faqTokenSets = new ArrayList<>();
        this.faqTokenDocFreq = new HashMap<>();

        for (FaqEntry entry : faq) {
            Set<String> tokens = tokenize(entry.question);
            faqTokenSets.add(tokens);
            for (String t : tokens) {
                faqTokenDocFreq.put(t, faqTokenDocFreq.getOrDefault(t, 0) + 1);
            }
        }
    }

    public static String normalizeAndStripPunct(String s) {
        s = s.toLowerCase(Locale.ROOT).trim();
        // replace non letters/digits with space
        return s.replaceAll("[^a-z0-9]+", " ").trim();
    }

    public static Set<String> tokenize(String s) {
        String norm = normalizeAndStripPunct(s);
        if (norm.isEmpty()) return new HashSet<>();
        String[] parts = norm.split("\\s+");
        Set<String> out = new HashSet<>();
        for (String p : parts) {
            if (p.length() < 2) continue;
            out.add(p);
        }
        return out;
    }

    public static class Reply {
        public final String answer;
        public final double confidence;
        public final List<String> suggestions;

        public Reply(String answer, double confidence, List<String> suggestions) {
            this.answer = answer;
            this.confidence = confidence;
            this.suggestions = suggestions;
        }
    }

    public Reply reply(String userMessage) {
        Set<String> userTokens = tokenize(userMessage);
        if (userTokens.isEmpty()) {
            return new Reply("Please type a message with a few keywords.", 0.0, suggestionsFor(""));
        }

        int bestIdx = -1;
        double bestScore = -1;

        for (int i = 0; i < faqTokenSets.size(); i++) {
            Set<String> ft = faqTokenSets.get(i);
            if (ft.isEmpty()) continue;

            // Overlap scoring with mild length normalization
            int overlap = 0;
            for (String t : userTokens) {
                if (ft.contains(t)) overlap++;
            }
            // confidence: overlap / sqrt(userSize * faqSize)
            double denom = Math.sqrt((double) userTokens.size() * (double) ft.size());
            double score = denom == 0 ? 0.0 : overlap / denom;

            // small boost for rarer tokens
            // (simple idf-like boost, not required but helps a bit)
            double boost = 0.0;
            for (String t : userTokens) {
                if (!ft.contains(t)) continue;
                int df = faqTokenDocFreq.getOrDefault(t, 1);
                double idf = Math.log((faq.size() + 1.0) / (df + 1.0));
                boost += idf;
            }
            score += 0.02 * boost;

            if (score > bestScore) {
                bestScore = score;
                bestIdx = i;
            }
        }

        if (bestIdx >= 0 && bestScore >= minConfidence) {
            return new Reply(faq.get(bestIdx).answer, bestScore, new ArrayList<>());
        }

        // fallback: show top 3 similar questions
        List<Integer> ranked = rankTop(userTokens, 3);
        List<String> suggestions = new ArrayList<>();
        for (int idx : ranked) suggestions.add(faq.get(idx).question);

        String fallback = "I’m not fully sure I understand. Try rephrasing, or choose one of these topics.";
        return new Reply(fallback, bestScore, suggestions);
    }

    private List<Integer> suggestionsFor(String userMessage) {
        // currently unused; kept for future extension
        return new ArrayList<>();
    }

    private List<Integer> rankTop(Set<String> userTokens, int k) {
        List<Integer> idxs = new ArrayList<>();
        for (int i = 0; i < faqTokenSets.size(); i++) idxs.add(i);

        idxs.sort((a, b) -> Double.compare(score(userTokens, b), score(userTokens, a)));
        if (idxs.size() > k) return idxs.subList(0, k);
        return idxs;
    }

    private double score(Set<String> userTokens, int faqIdx) {
        Set<String> ft = faqTokenSets.get(faqIdx);
        int overlap = 0;
        for (String t : userTokens) {
            if (ft.contains(t)) overlap++;
        }
        double denom = Math.sqrt((double) userTokens.size() * (double) ft.size());
        double sc = denom == 0 ? 0.0 : overlap / denom;
        return sc;
    }
}

