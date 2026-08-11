<template>
  <aside :class="[
      'fixed mt-16 flex flex-col lg:mt-0 top-0 px-5 left-0 bg-white dark:bg-gray-900 dark:border-gray-800 text-gray-900 h-screen transition-all duration-300 ease-in-out z-99999 border-r border-gray-200',
      {
        'lg:w-[290px]': isExpanded || isMobileOpen || isHovered,
        'lg:w-[90px]': !isExpanded && !isHovered,
        'translate-x-0 w-[290px]': isMobileOpen,
        '-translate-x-full': !isMobileOpen,
        'lg:translate-x-0': true,
      },
    ]"
    @mouseenter="!isExpanded && (isHovered = true)"
    @mouseleave="isHovered = false"
  >
    <div :class="[
        'py-8 flex',
        !isExpanded && !isHovered ? 'lg:justify-center' : 'justify-start',
      ]"
    >
      <router-link to="/admin">
        <h2
          v-if="isExpanded || isHovered || isMobileOpen"
          class="dark:hidden text-black text-lg font-semibold"
        >
          Admin
        </h2>

        <h2
          v-if="isExpanded || isHovered || isMobileOpen"
          class="hidden dark:block text-white text-lg font-semibold"
        >
          Admin
        </h2>
      </router-link>
    </div>
    <div 
      class="flex flex-col overflow-y-auto duration-300 ease-linear no-scrollbar"
    >
      <nav class="mb-6">
        <div class="flex flex-col gap-4">
          <div v-for="(menuGroup, groupIndex) in menuGroups" :key="groupIndex">
            <h2
              :class="[
                'mb-4 text-xs uppercase flex leading-[20px] text-gray-400',
                !isExpanded && !isHovered
                  ? 'lg:justify-center'
                  : 'justify-start',
              ]"
            >
              <template v-if="isExpanded || isHovered || isMobileOpen">
                {{ menuGroup.title }}
              </template>
              <HorizontalDots v-else />
            </h2>
            <ul class="flex flex-col gap-4">
              <li v-for="(item, index) in menuGroup.items" :key="item.name">
                <button
                  v-if="item.subItems"
                  @click="toggleSubmenu(groupIndex, index)"
                  :class="[
                    'menu-item group w-full',
                    {
                      'menu-item-active': isSubmenuOpen(groupIndex, index),
                      'menu-item-inactive': !isSubmenuOpen(groupIndex, index),
                    },
                    !isExpanded && !isHovered
                      ? 'lg:justify-center'
                      : 'lg:justify-start',
                  ]"
                >
                  <span
                    :class="[
                      isSubmenuOpen(groupIndex, index)
                        ? 'menu-item-icon-active'
                        : 'menu-item-icon-inactive',
                    ]"
                  >
                    <component :is="item.icon" />
                  </span>
                  <span
                    v-if="isExpanded || isHovered || isMobileOpen"
                    class="menu-item-text"
                    >{{ item.name }}</span
                  >
                  <ChevronDownIcon
                    v-if="isExpanded || isHovered || isMobileOpen"
                    :class="[
                      'ml-auto w-5 h-5 transition-transform duration-200',
                      {
                        'rotate-180 text-brand-500': isSubmenuOpen(
                          groupIndex,
                          index
                        ),
                      },
                    ]"
                  />
                </button>
                <router-link
                  v-else-if="item.path"
                  :to="item.path"
                  :class="[
                    'menu-item group',
                    {
                      'menu-item-active': isActive(item.path),
                      'menu-item-inactive': !isActive(item.path),
                    },
                  ]"
                >
                  <span
                    :class="[
                      isActive(item.path)
                        ? 'menu-item-icon-active'
                        : 'menu-item-icon-inactive',
                    ]"
                  >
                    <component :is="item.icon" />
                  </span>
                  <span
                    v-if="isExpanded || isHovered || isMobileOpen"
                    class="menu-item-text"
                    >{{ item.name }}</span
                  >
                </router-link>
                <transition
                  @enter="startTransition"
                  @after-enter="endTransition"
                  @before-leave="startTransition"
                  @after-leave="endTransition"
                >
                  <div
                    v-show="
                      isSubmenuOpen(groupIndex, index) &&
                      (isExpanded || isHovered || isMobileOpen)
                    "
                  >
                    <ul class="mt-2 space-y-1 ml-9">
                      <li v-for="subItem in item.subItems" 
                        :key="subItem.name">
                        <router-link
                          :to="subItem.path"
                          :class="[
                            'menu-dropdown-item',
                            {
                              'menu-dropdown-item-active': isActive(
                                subItem.path
                              ),
                              'menu-dropdown-item-inactive': !isActive(
                                subItem.path
                              ),
                            },
                          ]"
                        >
                          {{ subItem.name }}
                          <span class="flex items-center gap-1 ml-auto">
                            <span
                              v-if="subItem.new"
                              :class="[
                                'menu-dropdown-badge',
                                {
                                  'menu-dropdown-badge-active': isActive(
                                    subItem.path
                                  ),
                                  'menu-dropdown-badge-inactive': !isActive(
                                    subItem.path
                                  ),
                                },
                              ]"
                            >
                              new
                            </span>
                            <span
                              v-if="subItem.pro"
                              :class="[
                                'menu-dropdown-badge',
                                {
                                  'menu-dropdown-badge-active': isActive(
                                    subItem.path
                                  ),
                                  'menu-dropdown-badge-inactive': !isActive(
                                    subItem.path
                                  ),
                                },
                              ]"
                            >
                              pro
                            </span>
                          </span>
                        </router-link>
                      </li>
                    </ul>
                  </div>
                </transition>
              </li>
            </ul>
          </div>
        </div>
      </nav>
      
    </div>
  </aside>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";
import { useRoute } from 'vue-router'

import {
  GridIcon,
  HorizontalDots,
  ChevronDownIcon,
  BoxIcon,
  BoxCloseIcon,
  EmailIcon,
  FileIcon,
  UserIcon,
  officeIcon,
  SejourIcon,
  HeroIcon,
  ChatIcon,
  StocklistIcon,
  GroupInventaireIcon

} from "../../../icons"

import { useSidebar } from '@/composables/useSidebar'
import SidebarWidget from "./SidebarWidget.vue";

const route = useRoute()

const { isExpanded, isMobileOpen, isHovered, openSubmenu } = useSidebar()

//typage pour typescripte
type SubMenuItem = {
  name: string
  path: string
  pro?: boolean
  new?: boolean
}

type MenuItem = {
  name: string
  icon?: any
  path?: string
  subItems?: SubMenuItem[]
}

type MenuGroup = {
  title: string
  items: MenuItem[]
}

const menuGroups: MenuGroup[] = [
  {
    title: "Menu",
    items: [
      {
        icon: GridIcon,
        name: 'Tableau de bord',
        path: '/admin',
      },
      {
        icon: UserIcon,
        name: 'Gestion utilisateurs',
        subItems: [
          {name: 'Ajout utilisateur', path: '/admin/users', pro: false},
          {name: 'liste utilisateurs', path: '/admin/liste_users', pro: false},
        ]
        
      },
      {
        icon: officeIcon,
        name: 'Box office',
        path: '/admin/box',
      },
      {
        icon: BoxCloseIcon,
        name: 'Consommables',
        path: '/admin/consommables',
      },
      {
        icon: GroupInventaireIcon,
        name: 'Inventaire',
        path: '/admin/inventaire',
      },
      {
        icon: StocklistIcon,
        name: 'Gestion Stock',
        path: '/admin/stockBureau',
      },
      {
        icon: EmailIcon,
        name: 'Emails destinataires',
        path: '/admin/emails',
      },
      {
        icon: SejourIcon,
        name: 'sejour visa',
        path: '/admin/sejour'
      },
      {
        icon: ChatIcon,
        name: 'Discussion instantané',
        path: '/admin/messaging'
      },
      {
        icon: HeroIcon,
        name: 'Incidents',
        subItems: [
          {name: 'Système', path: '/admin/systeme', pro: false},
          {name: 'Materièls', path: '/admin/materiel', pro: false},
          {name: 'Réseau', path: '/admin/reseau', pro: false}
        ]
      },
      {
        icon: FileIcon,
        name: 'Rapports',
        subItems: [
          {name: 'rediger', path: '/admin/rediger', pro: false},
          {name: 'consulter', path: '/admin/consulter'}
        ] 
      },
    ]
  }    
]
    

const isActive = (path: string) => route.path.startsWith(path)

const toggleSubmenu = (groupIndex:number, itemIndex:number) => {
  const key = `${groupIndex}-${itemIndex}`;
  openSubmenu.value = openSubmenu.value === key ? null : key;
};

const isAnySubmenuRouteActive = computed(() => {
  return menuGroups.some((group) =>
    group.items.some(
      (item) =>
        item.subItems && item.subItems.some((subItem) => isActive(subItem.path))
    )
  );
});

const isSubmenuOpen = (groupIndex:number, itemIndex:number):boolean => {
  const key = `${groupIndex}-${itemIndex}`;

  const group = menuGroups[groupIndex]
  const item = group?.items[itemIndex]

  if (!item || !item.subItems) return false

  return (
    openSubmenu.value === key ||
    (isAnySubmenuRouteActive.value &&
      item.subItems.some((subItem) => isActive(subItem.path)))
  )
  /*return (
    openSubmenu.value === key ||
    (isAnySubmenuRouteActive.value &&
      (menuGroups[groupIndex]?.items[itemIndex]?.subItems?.some((subItem) =>
        isActive(subItem.path) ?? false)
      ))
  )*/
};

const startTransition = (el: Element) => {
  const element = el as HTMLElement

  element.style.height = "auto";
  const height = element.scrollHeight;
  element.style.height = "0px";
  element.offsetHeight; // force reflow
  element.style.height = height + "px";
};

const endTransition = (el: Element) => {
  const element = el as HTMLElement
  
  element.style.height = "";
};
</script>
