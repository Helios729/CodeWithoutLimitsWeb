import { useRouter } from "expo-router";
import { LinearGradient } from "expo-linear-gradient";
import * as Linking from "expo-linking";
import * as WebBrowser from "expo-web-browser";
import React, { useEffect, useState } from "react";
import {
  Dimensions,
  Platform,
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
} from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import Svg, {
  Defs,
  LinearGradient as SvgLinearGradient,
  Path,
  Stop,
} from "react-native-svg";

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
    if (user) router.replace("/");
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
      router.replace("/");
    } catch (e: any) {
      setError(e?.message || "Sign-in failed. Please try again.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <View style={styles.bg}>
      <KenscoffMountains />

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
            By signing in, you agree to be a co-learner. We do not sell
            community language data without consent.
          </Text>
        </View>
      </SafeAreaView>
    </View>
  );
}

// Misty, atmospheric silhouette of the Kenscoff mountains (Haiti).
// Four overlapping ridges fade from soft pale grey (far) to deep slate
// (foreground), with a warm sepia dawn glow at the horizon. Built with
// react-native-svg so it renders crisp on any pixel density and never
// pixelates the way the old photo did.
function KenscoffMountains() {
  const { width, height } = Dimensions.get("window");
  // Cap the SVG height proportionally so the silhouette feels grounded.
  const svgHeight = Math.max(height, 600);
  return (
    <View style={styles.mountainWrap} pointerEvents="none">
      {/* Sky: cream → warm sepia haze */}
      <LinearGradient
        colors={["#F7F5F0", "#F2E6D4", "#E6CDB0"]}
        locations={[0, 0.55, 1]}
        style={StyleSheet.absoluteFill}
      />
      <Svg
        width={width}
        height={svgHeight}
        viewBox="0 0 800 600"
        preserveAspectRatio="xMidYMax slice"
        style={styles.mountainSvg}
      >
        <Defs>
          {/* Warm sepia glow near the horizon */}
          <SvgLinearGradient id="dawn" x1="0" y1="0.4" x2="0" y2="1">
            <Stop offset="0" stopColor="#E6B87D" stopOpacity="0" />
            <Stop offset="0.35" stopColor="#D89A5C" stopOpacity="0.35" />
            <Stop offset="1" stopColor="#A0826D" stopOpacity="0.55" />
          </SvgLinearGradient>
          {/* Furthest ridge — pale misty slate */}
          <SvgLinearGradient id="ridge1" x1="0" y1="0" x2="0" y2="1">
            <Stop offset="0" stopColor="#B6B5AE" stopOpacity="0.55" />
            <Stop offset="1" stopColor="#9C9A91" stopOpacity="0.85" />
          </SvgLinearGradient>
          {/* Mid ridge — sepia-warmed slate */}
          <SvgLinearGradient id="ridge2" x1="0" y1="0" x2="0" y2="1">
            <Stop offset="0" stopColor="#8E8576" stopOpacity="0.85" />
            <Stop offset="1" stopColor="#6E6657" stopOpacity="1" />
          </SvgLinearGradient>
          {/* Near ridge — deeper sepia slate */}
          <SvgLinearGradient id="ridge3" x1="0" y1="0" x2="0" y2="1">
            <Stop offset="0" stopColor="#6B5E4A" stopOpacity="1" />
            <Stop offset="1" stopColor="#4F4636" stopOpacity="1" />
          </SvgLinearGradient>
          {/* Foreground silhouette — darkest, slate grey w/ warm undertone */}
          <SvgLinearGradient id="ridge4" x1="0" y1="0" x2="0" y2="1">
            <Stop offset="0" stopColor="#3F3A30" stopOpacity="1" />
            <Stop offset="1" stopColor="#2C2922" stopOpacity="1" />
          </SvgLinearGradient>
        </Defs>

        {/* Horizon dawn wash */}
        <Path d="M0,180 L800,180 L800,600 L0,600 Z" fill="url(#dawn)" />

        {/* Far ridge — gentle rolling, deeper into the haze */}
        <Path
          d="M0,260
             C 60,220 110,250 160,232
             C 220,210 260,238 310,220
             C 360,205 400,232 450,218
             C 510,200 550,232 600,218
             C 660,202 720,232 800,212
             L 800,600 L 0,600 Z"
          fill="url(#ridge1)"
        />

        {/* Mid ridge — defined Kenscoff peaks */}
        <Path
          d="M0,360
             L 70,300
             L 130,338 L 190,278
             L 240,332 L 300,290
             L 360,328 L 420,274
             L 480,336 L 540,302
             L 600,338 L 660,288
             L 720,334 L 800,304
             L 800,600 L 0,600 Z"
          fill="url(#ridge2)"
        />

        {/* Near ridge — sharper, taller peaks */}
        <Path
          d="M0,440
             L 50,408
             L 110,368
             L 170,420
             L 230,352
             L 290,412
             L 350,368
             L 410,340
             L 470,408
             L 530,360
             L 590,412
             L 650,370
             L 720,412
             L 800,388
             L 800,600 L 0,600 Z"
          fill="url(#ridge3)"
        />

        {/* Foreground silhouette */}
        <Path
          d="M0,520
             L 60,490
             L 130,518
             L 200,478
             L 280,516
             L 360,482
             L 440,518
             L 520,486
             L 600,520
             L 680,490
             L 760,518
             L 800,506
             L 800,600 L 0,600 Z"
          fill="url(#ridge4)"
        />
      </Svg>

      {/* Soft top-down mist veil to lift the hero text off the ridges */}
      <LinearGradient
        colors={[
          "rgba(247,245,240,0.55)",
          "rgba(247,245,240,0.18)",
          "rgba(247,245,240,0)",
        ]}
        locations={[0, 0.4, 0.65]}
        style={StyleSheet.absoluteFill}
        pointerEvents="none"
      />
    </View>
  );
}

const styles = StyleSheet.create({
  bg: { flex: 1, backgroundColor: colors.bg },
  mountainWrap: {
    ...StyleSheet.absoluteFillObject,
    overflow: "hidden",
  },
  mountainSvg: {
    position: "absolute",
    left: 0,
    right: 0,
    bottom: 0,
  },
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
