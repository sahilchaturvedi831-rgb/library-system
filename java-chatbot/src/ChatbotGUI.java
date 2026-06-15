
import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.IOException;
import java.nio.file.Path;
import java.util.List;

public class ChatbotGUI extends JFrame {

    private final JTextArea chatArea;
    private final JTextField inputField;
    private final JButton sendButton;

    private final JButton faqButton;

    private final Chatbot bot;

    public ChatbotGUI(Chatbot bot) {
        super("AI FAQ Chatbot (Java Swing)");
        this.bot = bot;

        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setSize(720, 520);
        setLocationRelativeTo(null);

        chatArea = new JTextArea();
        chatArea.setEditable(false);
        chatArea.setLineWrap(true);
        chatArea.setWrapStyleWord(true);

        JScrollPane scrollPane = new JScrollPane(chatArea);

        inputField = new JTextField();
        sendButton = new JButton("Send");
        faqButton = new JButton("FAQ suggestions");

        JPanel bottom = new JPanel(new BorderLayout(8, 8));
        bottom.setBorder(BorderFactory.createEmptyBorder(8, 8, 8, 8));
        bottom.add(inputField, BorderLayout.CENTER);

        JPanel controls = new JPanel(new FlowLayout(FlowLayout.RIGHT));
        controls.add(faqButton);
        controls.add(sendButton);
        bottom.add(controls, BorderLayout.EAST);

        getContentPane().setLayout(new BorderLayout());
        getContentPane().add(scrollPane, BorderLayout.CENTER);
        getContentPane().add(bottom, BorderLayout.SOUTH);

        sendButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                onSend();
            }
        });

        inputField.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                onSend();
            }
        });

        faqButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                appendBotMessage("You can ask things like: 'How do I run the program?', 'How do I add more FAQs?', or 'What is this chatbot?' ");
            }
        });

        appendBotMessage("Hi! Ask me a Frequently Asked Question about this chatbot project.");
    }

    private void onSend() {
        String msg = inputField.getText();
        if (msg == null) msg = "";
        msg = msg.trim();
        if (msg.isEmpty()) return;

        appendUserMessage(msg);
        inputField.setText("");

        Chatbot.Reply reply = bot.reply(msg);
        appendBotMessage(reply.answer);
        if (reply.suggestions != null && !reply.suggestions.isEmpty()) {
            StringBuilder sb = new StringBuilder();
            sb.append("Suggestions:\n");
            for (String s : reply.suggestions) sb.append("- ").append(s).append("\n");
            appendBotMessage(sb.toString().trim());
        }
    }

    private void appendUserMessage(String msg) {
        chatArea.append("You: " + msg + "\n");
        chatArea.setCaretPosition(chatArea.getDocument().getLength());
    }

    private void appendBotMessage(String msg) {
        chatArea.append("Bot: " + msg + "\n\n");
        chatArea.setCaretPosition(chatArea.getDocument().getLength());
    }

    public static void main(String[] args) {
        try {
            Path faqPath = Path.of("faq.json");
            // When launched from build_and_run.bat, working dir is java-chatbot/
            // but if IDE changes it, try fallback next to jar/classes.
            if (!faqPath.toFile().exists()) {
                faqPath = Path.of("java-chatbot/faq.json");
            }

            List<JsonFaqLoader.FaqEntry> faq = JsonFaqLoader.loadFaq(faqPath);
            Chatbot bot = new Chatbot(faq);

            SwingUtilities.invokeLater(() -> {
                ChatbotGUI gui = new ChatbotGUI(bot);
                gui.setVisible(true);
            });
        } catch (IOException ex) {
            ex.printStackTrace();
            SwingUtilities.invokeLater(() -> {
                JOptionPane.showMessageDialog(null,
                        "Failed to load faq.json: " + ex.getMessage(),
                        "Error", JOptionPane.ERROR_MESSAGE);
            });
        }
    }
}

