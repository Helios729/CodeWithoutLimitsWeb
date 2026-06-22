import React from "react";
import { StyleSheet, Text, View } from "react-native";

import { colors, radius } from "@/src/theme";
import { useAuth } from "@/src/context/AuthContext";

// Always-visible meter in the header. Shows tier + the most-restrictive
// remaining capacity so the learner knows when they'll hit a wall.
export default function TokenMeter() {
  const { usage } = useAuth();
  if (!usage) {
    return (
      <View style={styles.pill} testID="token-meter">
        <Text style={styles.label}>Free</Text>
      </View>
    );
  }

  let label = "";
  let pct = 0;

  if (usage.tier === "day_pass") {
    const tokenLeft = Math.max(0, usage.daily_tokens_cap - usage.daily_tokens_used);
    const promptLeft = Math.max(0, usage.daily_prompts_cap - usage.daily_prompts_used);
    label = `${promptLeft}/${usage.daily_prompts_cap} prompts · ${Math.round(
      tokenLeft / 1000,
    )}k tok`;
    pct = Math.min(
      (usage.daily_prompts_used / Math.max(1, usage.daily_prompts_cap)) * 100,
      (usage.daily_tokens_used / Math.max(1, usage.daily_tokens_cap)) * 100,
    );
  } else if (usage.tier === "monthly") {
    const left = Math.max(0, usage.monthly_tokens_cap - usage.monthly_tokens_used);
    label = `${Math.round(left / 1000)}k / ${Math.round(usage.monthly_tokens_cap / 1000)}k tok`;
    pct = (usage.monthly_tokens_used / Math.max(1, usage.monthly_tokens_cap)) * 100;
  } else {
    label = "Free — upgrade for AI";
  }

  pct = Math.max(0, Math.min(100, pct));
  const filled = Math.round(pct);

  return (
    <View style={styles.pill} testID="token-meter">
      <View style={styles.bar}>
        <View style={[styles.fill, { width: `${filled}%` }]} />
      </View>
      <Text style={styles.label} numberOfLines={1}>
        {label}
      </Text>
    </View>
  );
}

const styles = StyleSheet.create({
  pill: {
    flexDirection: "row",
    alignItems: "center",
    paddingHorizontal: 12,
    paddingVertical: 6,
    backgroundColor: colors.surface,
    borderRadius: radius.pill,
    borderWidth: 1,
    borderColor: colors.border,
    gap: 8,
    maxWidth: 240,
  },
  bar: {
    width: 56,
    height: 6,
    borderRadius: 4,
    backgroundColor: colors.border,
    overflow: "hidden",
  },
  fill: {
    height: "100%",
    backgroundColor: colors.brandSecondary,
  },
  label: {
    fontSize: 12,
    fontWeight: "600",
    color: colors.text,
  },
});
