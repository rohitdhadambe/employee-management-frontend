<template>
  <q-layout view="hHh lpR fFf">
    <q-header elevated class="bg-white text-grey-9">
      <q-toolbar class="q-px-lg">
        <q-btn 
          flat 
          dense 
          round 
          icon="menu"
          @click="toggleDrawer"
          class="lt-lg"
        />

        <q-toolbar-title class="row items-center">
          <div class="row items-center no-wrap">
            <q-avatar size="36px" color="primary" text-color="white" class="q-mr-sm">
              <strong>EM</strong>
            </q-avatar>
            <div>
              <div class="text-weight-bold text-h6">Employee Management System</div>
            </div>
          </div>
        </q-toolbar-title>

        <q-space />

        <div class="row items-center q-gutter-sm">
          <q-btn 
            flat 
            dense 
            round 
            icon="notifications_none"
            color="grey-8"
          >
            <q-badge color="red" floating rounded>3</q-badge>
            <q-tooltip>Notifications</q-tooltip>
          </q-btn>

          <q-separator vertical inset class="q-mx-sm" />

          <q-btn-dropdown 
            flat 
            dense
            dropdown-icon="keyboard_arrow_down"
            class="q-px-sm"
          >
            <template v-slot:label>
              <div class="row items-center no-wrap">
                <q-avatar size="32px" color="blue-grey-2" text-color="blue-grey-9" class="q-mr-sm">
                  <q-icon name="person_outline" />
                </q-avatar>

                <div class="q-ml-sm text-left gt-sm">
                  <div class="text-weight-medium text-body2">Rohit Dhadambe</div>
                  <div class="text-caption text-grey-6">Administrator</div>
                </div>
              </div>
            </template>

            <q-list style="min-width: 200px">
              <q-item clickable v-close-popup>
                <q-item-section avatar>
                  <q-icon name="person" />
                </q-item-section>
                <q-item-section>Profile</q-item-section>
              </q-item>

              <q-item clickable v-close-popup>
                <q-item-section avatar>
                  <q-icon name="settings" />
                </q-item-section>
                <q-item-section>Settings</q-item-section>
              </q-item>

              <q-separator />

              <q-item clickable v-close-popup>
                <q-item-section avatar>
                  <q-icon name="logout" color="negative" />
                </q-item-section>
                <q-item-section class="text-negative">Logout</q-item-section>
              </q-item>
            </q-list>
          </q-btn-dropdown>
        </div>
      </q-toolbar>
    </q-header>

    <q-drawer 
      v-model="drawerOpen" 
      show-if-above
      :width="260"
      :breakpoint="1024"
      bordered
      class="bg-grey-1"
    >
      <q-scroll-area class="fit">
        <q-list padding class="q-pa-md">
          <q-item-label header class="text-grey-8 text-weight-bold q-px-sm q-mb-sm">
            MAIN MENU
          </q-item-label>

          <q-item 
            clickable 
            v-ripple
            :active="isActive('/')"
            @click="handleNavigate('/')"
            active-class="bg-primary text-white"
            class="nav-item q-mb-xs"
          >
            <q-item-section avatar>
              <q-icon name="dashboard" />
            </q-item-section>
            <q-item-section>
              <q-item-label>Dashboard</q-item-label>
            </q-item-section>
          </q-item>

          <q-item 
            clickable 
            v-ripple
            :active="isActive('/employees')"
            @click="handleNavigate('/')"
            active-class="bg-primary text-white"
            class="nav-item q-mb-xs"
          >
            <q-item-section avatar>
              <q-icon name="people" />
            </q-item-section>
            <q-item-section>
              <q-item-label>Employees</q-item-label>
            </q-item-section>
          </q-item>

          <q-item 
            clickable 
            v-ripple
            class="nav-item q-mb-xs"
          >
            <q-item-section avatar>
              <q-icon name="assessment" />
            </q-item-section>
            <q-item-section>
              <q-item-label>Reports</q-item-label>
            </q-item-section>
          </q-item>

          <q-item 
            clickable 
            v-ripple
            class="nav-item q-mb-xs"
          >
            <q-item-section avatar>
              <q-icon name="event" />
            </q-item-section>
            <q-item-section>
              <q-item-label>Calendar</q-item-label>
            </q-item-section>
          </q-item>

          <q-separator class="q-my-lg" />

          <q-item-label header class="text-grey-8 text-weight-bold q-px-sm q-mb-sm">
            SETTINGS
          </q-item-label>

          <q-item 
            clickable 
            v-ripple
            class="nav-item q-mb-xs"
          >
            <q-item-section avatar>
              <q-icon name="tune" />
            </q-item-section>
            <q-item-section>
              <q-item-label>Preferences</q-item-label>
            </q-item-section>
          </q-item>

          <q-item 
            clickable 
            v-ripple
            class="nav-item q-mb-xs"
          >
            <q-item-section avatar>
              <q-icon name="help_outline" />
            </q-item-section>
            <q-item-section>
              <q-item-label>Help</q-item-label>
            </q-item-section>
          </q-item>
        </q-list>

        <q-separator />

        <div class="q-pa-md text-center">
          <div class="text-caption text-grey-6">Version 1.0.0</div>
          <div class="text-caption text-grey-5">© 2025 rohitdhadambe</div>
        </div>
      </q-scroll-area>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import { useRouter, useRoute } from 'vue-router';

export default defineComponent({
  name: 'MainLayout',

  setup() {
    const router = useRouter();
    const route = useRoute();
    const drawerOpen = ref(true);

    const toggleDrawer = (): void => {
      drawerOpen.value = !drawerOpen.value;
    };

    const handleNavigate = (path: string): void => {
      router.push(path).catch(err => console.error(err));
    };

    const isActive = (path: string): boolean => {
      return route.path === path;
    };

    return {
      drawerOpen,
      toggleDrawer,
      handleNavigate,
      isActive,
    };
  },
});
</script>

<style lang="scss" scoped>
.nav-item {
  border-radius: 8px;
  transition: all 0.2s ease;
  &:hover:not(.q-item--active) {
    background-color: rgba(0, 0, 0, 0.05);
  }
}

.q-toolbar {
  min-height: 64px;
}
</style>