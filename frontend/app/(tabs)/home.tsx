import { Ionicons } from "@expo/vector-icons";
import { useFocusEffect, useRouter } from "expo-router";
import React, { useCallback } from "react";
import {
  RefreshControl,
  ScrollView,
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
} from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";

import TokenMeter from "@/src/components/TokenMeter";
import { useAuth } from "@/src/context/AuthContext";
import { colors, radius, spacing } from "@/src/theme";

const sprints = [
  { window: "06:00–06:15", title: "Wake & charge", task: "Solar/off-peak charge, draft today's learning intent on the locked screen." },
  { window: "12:00–12:15", title: "Capture", task: "Offline note + voice capture of one local-knowledge prompt." },
  { window: "16:00–16:15", title: "AI sprint", task: "Run your reusable prompt; refine an asset draft with low-token edits." },
  { window: "20:00–20:15", title: "Verify & share", task: "Human review checklist, then async sync when bandwidth allows." },
];

const modules = [
  { title: "AI Fundamentals", desc: "Agents, models, prompts." },
  { title: "Prompt Efficiency", desc: "One reusable prompt, low tokens." },
  { title: "Corpus Stewardship", desc: "Language data with consent." },
  { title: "Microenterprise", desc: "Asset → service menu → sale." },
];

export default function Home() {
  const { user, usage, refreshUsage } = useAuth();
  const router = useRouter();
  const [refreshing, setRefreshing] = React.useState(false);

  useFocusEffect(
    useCallback(() => {
      refreshUsage();
    }, [refreshUsage]),
  );

  const onRefresh = async () => {
    setRefreshing(true);
    await refreshUsage();
    setRefreshing(false);
  };

  const firstName = (user?.name || user?.email || "").split(/[\s@]/)[0];

  return (
    <SafeAreaView style={styles.safe} edges={["top"]}>
      <View style={styles.header}>
        <View style={{ flex: 1 }}>
          <Text style={styles.eyebrow}>Welcome back</Text>
          <Text style={styles.hello} testID="home-hello">
            {firstName ? `Hi, ${firstName}` : "Hello"}
          </Text>
        </View>
        <TokenMeter />
      </View>

      <ScrollView
        contentContainerStyle={styles.scroll}
        refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} />}
      >
        {usage?.blocked ? (
          <View style={styles.alert} testID="quota-alert">
            <Ionicons name="warning-outline" size={20} color={colors.brand} />
            <Text style={styles.alertText}>{usage.reason}</Text>
            <TouchableOpacity
              style={styles.alertBtn}
              onPress={() => router.push("/(tabs)/account")}
              testID="alert-upgrade-btn"
            >
              <Text style={styles.alertBtnText}>Upgrade</Text>
            </TouchableOpacity>
          </View>
        ) : usage?.tier === "free" ? (
          <View style={styles.alert} testID="byok-banner">
            <Ionicons name="key-outline" size={20} color={colors.brand} />
            <Text style={styles.alertText}>
              Free tier: paste your own Google Gemini key in the Studio to run AI prompts at zero platform cost.
            </Text>
            <TouchableOpacity
              style={styles.alertBtn}
              onPress={() => router.push("/(tabs)/studio")}
              testID="home-byok-btn"
            >
              <Text style={styles.alertBtnText}>Set key</Text>
            </TouchableOpacity>
          </View>
        ) : null}

        <TouchableOpacity
          style={styles.cta}
          onPress={() => router.push("/(tabs)/quiz")}
          testID="home-start-quiz-btn"
        >
          <View style={{ flex: 1 }}>
            <Text style={styles.ctaEyebrow}>Start a 15-minute sprint</Text>
            <Text style={styles.ctaTitle}>Try a 10-question quiz</Text>
            <Text style={styles.ctaSub}>
              Sourced from MIT, Stanford, Caltech, CMU, Berkeley.
            </Text>
          </View>
          <Ionicons name="arrow-forward" size={24} color="#fff" />
        </TouchableOpacity>

        <Text style={styles.sectionTitle}>Your daily rail</Text>
        <View style={styles.rail}>
          {sprints.map((s, i) => (
            <View key={s.window} style={styles.railRow}>
              <View style={styles.railNode}>
                <Text style={styles.railNodeText}>{i + 1}</Text>
              </View>
              <View style={{ flex: 1 }}>
                <Text style={styles.railTime}>{s.window}</Text>
                <Text style={styles.railTitle}>{s.title}</Text>
                <Text style={styles.railTask}>{s.task}</Text>
              </View>
            </View>
          ))}
        </View>

        <Text style={styles.sectionTitle}>Modules</Text>
        <View style={styles.cardGrid}>
          {modules.map((m) => (
            <View key={m.title} style={styles.card}>
              <Text style={styles.cardTitle}>{m.title}</Text>
              <Text style={styles.cardDesc}>{m.desc}</Text>
            </View>
          ))}
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safe: { flex: 1, backgroundColor: colors.bg },
  header: {
    flexDirection: "row",
    alignItems: "center",
    paddingHorizontal: spacing.lg,
    paddingTop: spacing.sm,
    paddingBottom: spacing.md,
    backgroundColor: colors.bg,
  },
  eyebrow: {
    color: colors.brand,
    fontSize: 11,
    fontWeight: "700",
    letterSpacing: 2,
    textTransform: "uppercase",
  },
  hello: { color: colors.text, fontSize: 24, fontWeight: "700" },
  scroll: { padding: spacing.lg, paddingTop: 0, gap: spacing.lg },
  alert: {
    flexDirection: "row",
    alignItems: "center",
    gap: spacing.sm,
    backgroundColor: "#FFF3EE",
    borderColor: colors.brand,
    borderWidth: 1,
    borderRadius: radius.card,
    padding: spacing.md,
  },
  alertText: { flex: 1, color: colors.text, fontSize: 13 },
  alertBtn: {
    backgroundColor: colors.brand,
    paddingHorizontal: 14,
    paddingVertical: 8,
    borderRadius: radius.pill,
  },
  alertBtnText: { color: "#fff", fontWeight: "700", fontSize: 13 },
  cta: {
    flexDirection: "row",
    alignItems: "center",
    backgroundColor: colors.brand,
    borderRadius: radius.card,
    padding: spacing.lg,
    gap: spacing.md,
  },
  ctaEyebrow: {
    color: "#FFEFE8",
    fontSize: 11,
    letterSpacing: 2,
    fontWeight: "700",
    textTransform: "uppercase",
  },
  ctaTitle: { color: "#fff", fontSize: 22, fontWeight: "700", marginTop: 4 },
  ctaSub: { color: "#FFE6DC", fontSize: 13, marginTop: 6 },
  sectionTitle: {
    color: colors.text,
    fontSize: 20,
    fontWeight: "700",
    marginTop: spacing.md,
  },
  rail: { backgroundColor: colors.surface, borderRadius: radius.card, padding: spacing.md, gap: spacing.md, borderWidth: 1, borderColor: colors.border },
  railRow: { flexDirection: "row", gap: spacing.md, alignItems: "flex-start" },
  railNode: {
    width: 32,
    height: 32,
    borderRadius: 16,
    backgroundColor: colors.brandSecondary,
    alignItems: "center",
    justifyContent: "center",
  },
  railNodeText: { color: "#fff", fontWeight: "700" },
  railTime: { color: colors.brand, fontSize: 11, fontWeight: "700", letterSpacing: 1 },
  railTitle: { color: colors.text, fontSize: 16, fontWeight: "600", marginTop: 2 },
  railTask: { color: colors.textSecondary, fontSize: 13, marginTop: 2 },
  cardGrid: { flexDirection: "row", flexWrap: "wrap", gap: spacing.md },
  card: {
    flexGrow: 1,
    flexBasis: "45%",
    backgroundColor: colors.surface,
    borderRadius: radius.card,
    padding: spacing.md,
    borderWidth: 1,
    borderColor: colors.border,
  },
  cardTitle: { color: colors.text, fontSize: 16, fontWeight: "700" },
  cardDesc: { color: colors.textSecondary, fontSize: 13, marginTop: 4 },
});
