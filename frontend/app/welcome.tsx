import { useRouter } from "expo-router";
import * as Linking from "expo-linking";
import * as WebBrowser from "expo-web-browser";
import React, { useEffect, useState } from "react";
import {
  ImageBackground,
  Platform,
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
} from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";

import { useAuth } from "@/src/context/AuthContext";
import ExpoGoBanner from "@/src/components/ExpoGoBanner";
import { colors, radius, spacing } from "@/src/theme";

// Emergent-managed Google auth flow. On web we navigate the whole tab;
// on native we open an in-app browser session and read the redirect URL
// from the result (plus a deep-link listener as a fallback).
export default function Welcome() {
  const router = useRouter();
  const { user, exchangeSessionId } = useAuth();
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    if (user) router.replace("/(tabs)/home");
  }, [user, router]);

  function parseSessionId(url: string): string | null {
    try {
      const u = new URL(url);
      const hash = u.hash.startsWith("#") ? u.hash.slice(1) : u.hash;
      const fromHash = new URLSearchParams(hash).get("session_id");
      const fromQuery = u.searchParams.get("session_id");
      return fromHash || fromQuery;
    } catch {
      const m = url.match(/session_id=([^&#]+)/);
      return m ? decodeURIComponent(m[1]) : null;
    }
  }

  async function handleSignIn() {
    setError("");
    setBusy(true);
    try {
      const redirectUrl =
        Platform.OS === "web" && typeof window !== "undefined"
          ? window.location.origin + "/"
          : Linking.createURL("auth");
      const authUrl = `https://auth.emergentagent.com/?redirect=${encodeURIComponent(
        redirectUrl,
      )}`;

      if (Platform.OS === "web") {
        if (typeof window !== "undefined") window.location.href = authUrl;
        return;
      }

      const result = await WebBrowser.openAuthSessionAsync(authUrl, redirectUrl);
      if (result.type !== "success" || !result.url) {
        setBusy(false);
        return;
      }
      const sid = parseSessionId(result.url);
      if (!sid) throw new Error("No session_id returned");
      await exchangeSessionId(sid);
      router.replace("/(tabs)/home");
    } catch (e: any) {
      setError(e?.message || "Sign-in failed. Please try again.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <ImageBackground
      source={{
        uri: "https://images.pexels.com/photos/9423069/pexels-photo-9423069.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940",
      }}
      style={styles.bg}
      imageStyle={{ opacity: 0.35 }}
    >
      <SafeAreaView style={styles.container} edges={["top", "bottom"]}>
        <View style={styles.brandRow}>
          <View style={styles.dot} />
          <Text style={styles.brandName}>Code Without Limits</Text>
        </View>

        <View style={styles.hero}>
          <Text style={styles.eyebrow} testID="welcome-eyebrow">
            Small AI · Mobile-first · Community-owned
          </Text>
          <Text style={styles.h1} testID="welcome-title">
            Turn local knowledge into ownable assets.
          </Text>
          <Text style={styles.lead}>
            A phone-first learning studio for low-bandwidth, energy-constrained
            contexts — built by Carline Romain for Mondial Connections &
            Community Changers Foundations.
          </Text>
        </View>

        <View style={styles.actions}>
          <ExpoGoBanner />
          <TouchableOpacity
            style={[styles.primaryBtn, busy && styles.disabled]}
            onPress={handleSignIn}
            disabled={busy}
            testID="login-google-btn"
            accessibilityLabel="Sign in with Google"
          >
            <Text style={styles.primaryBtnText}>
              {busy ? "Opening Google…" : "Sign in with Google"}
            </Text>
          </TouchableOpacity>
          {error ? (
            <Text style={styles.error} testID="auth-error">
              {error}
            </Text>
          ) : null}
          <Text style={styles.fine}>
            By signing in you agree to be a co-learner. We never sell community
            language data without consent.
          </Text>
        </View>
      </SafeAreaView>
    </ImageBackground>
  );
}

const styles = StyleSheet.create({
  bg: { flex: 1, backgroundColor: colors.bg },
  container: {
    flex: 1,
    padding: spacing.lg,
    justifyContent: "space-between",
  },
  brandRow: { flexDirection: "row", alignItems: "center", gap: spacing.sm },
  dot: {
    width: 14,
    height: 14,
    borderRadius: 7,
    backgroundColor: colors.brand,
  },
  brandName: { color: colors.text, fontWeight: "700", fontSize: 16 },
  hero: { gap: spacing.md },
  eyebrow: {
    color: colors.brand,
    letterSpacing: 2,
    fontSize: 11,
    fontWeight: "700",
    textTransform: "uppercase",
  },
  h1: {
    color: colors.text,
    fontSize: 38,
    fontWeight: "700",
    letterSpacing: -0.5,
    lineHeight: 42,
  },
  lead: {
    color: colors.textSecondary,
    fontSize: 16,
    lineHeight: 24,
  },
  actions: { gap: spacing.md },
  primaryBtn: {
    backgroundColor: colors.brand,
    borderRadius: radius.pill,
    paddingVertical: 16,
    alignItems: "center",
    justifyContent: "center",
  },
  disabled: { opacity: 0.7 },
  primaryBtnText: { color: "#fff", fontSize: 17, fontWeight: "600" },
  fine: {
    color: colors.textSecondary,
    fontSize: 12,
    lineHeight: 18,
    textAlign: "center",
  },
  error: {
    color: colors.danger,
    fontSize: 13,
    textAlign: "center",
  },
});
