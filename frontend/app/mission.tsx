import { Ionicons } from "@expo/vector-icons";
import { Stack, useRouter } from "expo-router";
import { ScrollView, StyleSheet, Text, TouchableOpacity, View } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";

import { storage } from "@/src/utils/storage";
import { colors, radius, spacing } from "@/src/theme";

const SEEN_KEY = "mission_seen";

// Shown once after sign-in. Persists a flag so returning learners go
// straight to Home. The "I understand" button is the only way forward,
// ensuring every learner has at least scrolled past the mission.
export default function MissionScreen() {
  const router = useRouter();

  async function continueIn() {
    await storage.setItem(SEEN_KEY, "1");
    router.replace("/(tabs)/home");
  }

  return (
    <SafeAreaView style={styles.safe} edges={["top", "bottom"]}>
      <Stack.Screen options={{ headerShown: false }} />
      <ScrollView contentContainerStyle={styles.scroll}>
        <View style={styles.iconWrap}>
          <Ionicons name="book-outline" size={36} color={colors.brand} />
        </View>
        <Text style={styles.eyebrow}>Before you begin</Text>
        <Text style={styles.h1}>Why Code Without Limits exists</Text>

        <Text style={styles.body}>
          The core mission for creating this app is to mitigate the digital, and
          now AI, divide. AI was used as a co-creator for this app —
          specifically, <Text style={styles.b}>Perplexity</Text> to verify
          research, and both <Text style={styles.b}>Claude 4.6</Text> and{" "}
          <Text style={styles.b}>ChatGPT 5.4</Text> to verify, and at times
          write or edit, code.
        </Text>

        <Text style={styles.body}>
          The lessons are presented in a format that eventually leads users to
          understand that coding through AI <Text style={styles.b}>without</Text>{" "}
          knowing anything about basic elements of computer science /
          computer engineering is <Text style={styles.b}>costly</Text> and
          potentially <Text style={styles.b}>hazardous</Text>.
        </Text>

        <Text style={styles.body}>
          It would be unethical for users to think they can build complex
          systems in an hour or less. All users must understand concepts such
          as <Text style={styles.b}>bandwidth</Text>,{" "}
          <Text style={styles.b}>throughput</Text>,{" "}
          <Text style={styles.b}>bottlenecks</Text>,{" "}
          <Text style={styles.b}>timeouts</Text>,{" "}
          <Text style={styles.b}>resets</Text>, and{" "}
          <Text style={styles.b}>memory</Text> to use the available AI tools
          effectively and efficiently — in terms of both time and cost.
        </Text>

        <Text style={styles.body}>
          Consequently, the sequence starts with an{" "}
          <Text style={styles.b}>Introduction to AI</Text> and ends with{" "}
          <Text style={styles.b}>Advanced HTML and API formation</Text> so
          students can comprehend that the foundation greatly matters — despite
          how much fun coding without foundational knowledge might seem.
        </Text>

        <Text style={styles.body}>
          Reading lists will eventually be added along with links to free open
          courses where users may obtain additional knowledge. If funds or
          grants permit on their end or ours, they can seek certification by
          paying the requisite fees on those platforms with which we have no
          affiliation.
        </Text>

        <TouchableOpacity
          style={styles.primaryBtn}
          onPress={continueIn}
          testID="mission-continue-btn"
        >
          <Text style={styles.primaryBtnText}>I understand — let's begin</Text>
        </TouchableOpacity>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safe: { flex: 1, backgroundColor: colors.bg },
  scroll: { padding: spacing.lg, gap: spacing.md, paddingBottom: 48 },
  iconWrap: {
    width: 64, height: 64, borderRadius: 32,
    backgroundColor: "#FFF3EE", alignItems: "center", justifyContent: "center",
    marginBottom: spacing.sm,
  },
  eyebrow: { color: colors.brand, fontSize: 11, fontWeight: "700", letterSpacing: 2, textTransform: "uppercase" },
  h1: { color: colors.text, fontSize: 26, fontWeight: "700", lineHeight: 32 },
  body: { color: colors.text, fontSize: 15, lineHeight: 23 },
  b: { fontWeight: "700" },
  primaryBtn: {
    backgroundColor: colors.brand,
    paddingVertical: 16, borderRadius: radius.pill,
    alignItems: "center", marginTop: spacing.md,
  },
  primaryBtnText: { color: "#fff", fontWeight: "700", fontSize: 16 },
});
