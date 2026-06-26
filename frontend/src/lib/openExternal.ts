import { Linking, Platform } from "react-native";

/**
 * Open an external URL safely from both Expo Web and native (iOS/Android).
 *
 * On Web, React Native's Linking.openURL replaces the current tab (and is
 * often blocked by the browser's anti-popup logic when triggered indirectly).
 * Using window.open with _blank + noopener keeps the app in place and opens
 * the destination in a new tab — which is what users actually expect when
 * tapping a reading-list or model card.
 *
 * On native we fall back to Linking, which delegates to the device's
 * default browser.
 */
export function openExternal(url: string | null | undefined): void {
  if (!url) return;
  try {
    if (Platform.OS === "web") {
      // eslint-disable-next-line no-undef
      window.open(url, "_blank", "noopener,noreferrer");
      return;
    }
    void Linking.openURL(url);
  } catch (_e) {
    // Last-resort fallback so a single bad URL never crashes the screen.
    try {
      void Linking.openURL(url);
    } catch (_ee) {
      /* noop */
    }
  }
}
