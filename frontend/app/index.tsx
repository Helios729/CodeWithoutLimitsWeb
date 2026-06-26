import { Redirect } from "expo-router";
import React, { useEffect, useState } from "react";
import { ActivityIndicator, StyleSheet, View } from "react-native";

import { storage } from "@/src/utils/storage";
import { useAuth } from "@/src/context/AuthContext";
import { colors } from "@/src/theme";

// Entry router. Signed-out → welcome. Signed-in but mission not yet
// acknowledged → /mission. Otherwise → main tabs.
export default function Index() {
  const { user, loading } = useAuth();
  const [seenMission, setSeenMission] = useState<boolean | null>(null);

  useEffect(() => {
    storage.getItem("mission_seen", "").then((v) => setSeenMission(!!v));
  }, []);

  if (loading || seenMission === null) {
    return (
      <View style={styles.center} testID="splash-loading">
        <ActivityIndicator color={colors.brand} size="large" />
      </View>
    );
  }
  if (!user) return <Redirect href="/welcome" />;
  if (!seenMission) return <Redirect href="/mission" />;
  return <Redirect href="/(tabs)/home" />;
}

const styles = StyleSheet.create({
  center: { flex: 1, alignItems: "center", justifyContent: "center", backgroundColor: colors.bg },
});
