import { Ionicons } from "@expo/vector-icons";
import { Stack, useRouter } from "expo-router";
import React, { useEffect, useState } from "react";
import {
  ActivityIndicator,
  Linking,
  ScrollView,
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
} from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";

import { api, unwrap } from "@/src/lib/api";
import { colors, radius, spacing } from "@/src/theme";

type Overview = { summary?: string; design_principles?: string[]; philosophy?: string };
type Languages = {
  instruction_language?: string;
  note?: string;
  translator_mode_core?: string[];
  translator_mode_best_effort?: string[];
  programme_languages?: string[];
};
type Week = { week?: number | string; theme?: string; focus?: string; activities?: string[] };
type ProgrammeStructure = { title?: string; access_note?: string; weeks?: Week[] };
type Workflow = { title?: string; stages?: any[]; note?: string; citations?: any[] };
type Reference = { key?: string; label?: string; title?: string; url?: string };

type ProgrammeResp = {
  title?: string;
  description?: string;
  overview?: Overview;
  core_rule?: string;
  languages?: Languages;
  programme_structure?: ProgrammeStructure;
  shared_energy_to_income_workflow?: Workflow;
  module_bank_intro?: { summary?: string; rationale?: string };
  references?: Reference[];
};

export default function Programme() {
  const router = useRouter();
  const [d, setD] = useState<ProgrammeResp | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    api
      .get<ProgrammeResp>("/programme")
      .then((r) => setD(r.data))
      .catch((e) => setError(unwrap(e).message));
  }, []);

  return (
    <SafeAreaView style={styles.safe} edges={["top"]}>
      <Stack.Screen options={{ headerShown: false }} />
      <View style={styles.header}>
        <TouchableOpacity onPress={() => router.back()} style={{ padding: 4 }} testID="programme-back-btn">
          <Ionicons name="chevron-back" size={22} color={colors.text} />
        </TouchableOpacity>
        <View style={{ flex: 1 }}>
          <Text style={styles.eyebrow}>About this programme</Text>
          <Text style={styles.h1} numberOfLines={2}>Code Without Limits</Text>
        </View>
      </View>

      {!d && !error ? (
        <ActivityIndicator color={colors.brand} style={{ marginTop: 32 }} />
      ) : error ? (
        <Text style={styles.error}>{error}</Text>
      ) : (
        <ScrollView contentContainerStyle={styles.scroll}>
          {d!.description ? (
            <Text style={styles.tagline}>{d!.description}</Text>
          ) : null}

          {d!.core_rule ? (
            <View style={styles.coreCard}>
              <Text style={styles.coreLabel}>Our core rule</Text>
              <Text style={styles.coreBody}>{d!.core_rule}</Text>
            </View>
          ) : null}

          {d!.overview?.summary ? (
            <View style={styles.section}>
              <View style={styles.sectionHeader}>
                <Ionicons name="book-outline" size={16} color={colors.brand} />
                <Text style={styles.sectionLabel}>Overview</Text>
              </View>
              <Text style={styles.sectionBody}>{d!.overview.summary}</Text>
              {(d!.overview.design_principles || []).length > 0 ? (
                <View style={styles.tagRow}>
                  {d!.overview!.design_principles!.map((p, i) => (
                    <Text key={i} style={styles.tag}>{p}</Text>
                  ))}
                </View>
              ) : null}
              {d!.overview.philosophy ? (
                <Text style={[styles.sectionBody, { fontStyle: "italic", marginTop: 8 }]}>
                  {d!.overview.philosophy}
                </Text>
              ) : null}
            </View>
          ) : null}

          {d!.programme_structure?.weeks && d!.programme_structure.weeks.length > 0 ? (
            <View style={styles.section}>
              <View style={styles.sectionHeader}>
                <Ionicons name="calendar-outline" size={16} color={colors.brand} />
                <Text style={styles.sectionLabel}>
                  {d!.programme_structure.title || "Programme structure"}
                </Text>
              </View>
              {d!.programme_structure.access_note ? (
                <Text style={[styles.sectionBody, { color: colors.brandSecondary }]}>
                  {d!.programme_structure.access_note}
                </Text>
              ) : null}
              {d!.programme_structure.weeks.map((w, i) => (
                <View key={i} style={styles.weekRow}>
                  <View style={styles.weekBadge}>
                    <Text style={styles.weekBadgeText}>W{w.week ?? i + 1}</Text>
                  </View>
                  <View style={{ flex: 1 }}>
                    <Text style={styles.weekTheme}>{w.theme || w.focus || "Week"}</Text>
                    {w.focus && w.focus !== w.theme ? (
                      <Text style={styles.sectionBody}>{w.focus}</Text>
                    ) : null}
                    {(w.activities || []).map((a, j) => (
                      <Text key={j} style={[styles.sectionBody, { marginTop: 2 }]}>
                        • {a}
                      </Text>
                    ))}
                  </View>
                </View>
              ))}
            </View>
          ) : null}

          {d!.languages ? (
            <View style={styles.section}>
              <View style={styles.sectionHeader}>
                <Ionicons name="language-outline" size={16} color={colors.brand} />
                <Text style={styles.sectionLabel}>Languages</Text>
              </View>
              {d!.languages.instruction_language ? (
                <Text style={styles.sectionBody}>
                  <Text style={{ fontWeight: "700" }}>Instruction: </Text>
                  {d!.languages.instruction_language}
                </Text>
              ) : null}
              {d!.languages.note ? (
                <Text style={styles.sectionBody}>{d!.languages.note}</Text>
              ) : null}
              {(d!.languages.programme_languages || []).length > 0 ? (
                <View style={styles.tagRow}>
                  {d!.languages.programme_languages!.map((l, i) => (
                    <Text key={i} style={styles.tag}>{l}</Text>
                  ))}
                </View>
              ) : null}
            </View>
          ) : null}

          {d!.module_bank_intro?.summary ? (
            <View style={styles.section}>
              <View style={styles.sectionHeader}>
                <Ionicons name="layers-outline" size={16} color={colors.brand} />
                <Text style={styles.sectionLabel}>Module bank</Text>
              </View>
              <Text style={styles.sectionBody}>{d!.module_bank_intro.summary}</Text>
              {d!.module_bank_intro.rationale ? (
                <Text style={[styles.sectionBody, { marginTop: 6 }]}>
                  {d!.module_bank_intro.rationale}
                </Text>
              ) : null}
              <TouchableOpacity
                onPress={() => router.push("/income")}
                style={styles.linkBtn}
                testID="programme-open-income-btn"
              >
                <Text style={styles.linkBtnText}>Open the 18 Income Modules</Text>
                <Ionicons name="arrow-forward" size={16} color="#fff" />
              </TouchableOpacity>
            </View>
          ) : null}

          {(d!.references || []).length > 0 ? (
            <View style={styles.section}>
              <View style={styles.sectionHeader}>
                <Ionicons name="library-outline" size={16} color={colors.brand} />
                <Text style={styles.sectionLabel}>References</Text>
              </View>
              {d!.references!.map((r, i) => (
                <TouchableOpacity
                  key={i}
                  onPress={() => (r.url ? Linking.openURL(r.url) : null)}
                  disabled={!r.url}
                  style={styles.citationRow}
                >
                  <Text style={styles.citationLabel}>{r.label || r.title || r.url}</Text>
                </TouchableOpacity>
              ))}
            </View>
          ) : null}
        </ScrollView>
      )}
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safe: { flex: 1, backgroundColor: colors.bg },
  header: {
    flexDirection: "row",
    alignItems: "center",
    gap: spacing.sm,
    paddingHorizontal: spacing.lg,
    paddingTop: spacing.sm,
    paddingBottom: spacing.md,
  },
  eyebrow: {
    color: colors.brand,
    fontSize: 11,
    fontWeight: "700",
    letterSpacing: 1.5,
    textTransform: "uppercase",
  },
  h1: { color: colors.text, fontSize: 22, fontWeight: "700" },
  scroll: { padding: spacing.lg, gap: spacing.md, paddingBottom: 40 },
  tagline: { color: colors.textSecondary, fontSize: 14, lineHeight: 22 },
  coreCard: {
    backgroundColor: "#EAF1EB",
    borderColor: colors.brandSecondary,
    borderWidth: 1,
    borderRadius: radius.card,
    padding: spacing.md,
    gap: 6,
  },
  coreLabel: {
    color: colors.brandSecondary,
    fontSize: 11,
    fontWeight: "700",
    letterSpacing: 1,
    textTransform: "uppercase",
  },
  coreBody: { color: colors.text, fontSize: 14, lineHeight: 21 },
  section: {
    backgroundColor: colors.surface,
    borderRadius: radius.card,
    borderWidth: 1,
    borderColor: colors.border,
    padding: spacing.md,
    gap: 8,
  },
  sectionHeader: { flexDirection: "row", alignItems: "center", gap: 8 },
  sectionLabel: { color: colors.text, fontSize: 14, fontWeight: "700" },
  sectionBody: { color: colors.textSecondary, fontSize: 13, lineHeight: 20 },
  tagRow: { flexDirection: "row", gap: 6, flexWrap: "wrap", marginTop: 4 },
  tag: {
    backgroundColor: colors.bg,
    color: colors.text,
    paddingHorizontal: 10,
    paddingVertical: 5,
    borderRadius: 999,
    fontSize: 12,
    fontWeight: "600",
    borderWidth: 1,
    borderColor: colors.border,
    overflow: "hidden",
  },
  weekRow: { flexDirection: "row", gap: spacing.md, alignItems: "flex-start", marginTop: 4 },
  weekBadge: {
    backgroundColor: colors.brand,
    borderRadius: 999,
    paddingHorizontal: 10,
    paddingVertical: 4,
    minWidth: 38,
    alignItems: "center",
  },
  weekBadgeText: { color: "#fff", fontWeight: "700", fontSize: 12 },
  weekTheme: { color: colors.text, fontSize: 14, fontWeight: "700" },
  linkBtn: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    gap: 8,
    backgroundColor: colors.brand,
    borderRadius: radius.pill,
    paddingVertical: 12,
    marginTop: 8,
  },
  linkBtnText: { color: "#fff", fontWeight: "700", fontSize: 14 },
  citationRow: { paddingVertical: 4 },
  citationLabel: { color: colors.brand, fontSize: 13, textDecorationLine: "underline" },
  error: { color: colors.danger, padding: spacing.lg },
});
