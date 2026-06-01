// 靠北娛樂城 - 站點全域配置
// 注意：此為預覽/開發版本，所有 demo 頁面均標記為 noindex

const SITE_CONFIG = {
  site_name: "靠北娛樂城",
  site_name_en: "Kao Bei Entertainment City",
  tagline: "線上娛樂城爭議紀錄與風險觀察資料庫",
  description: "靠北娛樂城是專注於線上娛樂城出金爭議、客服糾紛、優惠條款爭議等事件的紀錄與觀察平台。所有資料僅供參考，不構成任何投資或博弈建議。",
  base_url: "https://kaobei-casino.example.com",
  fun1399_url: "https://fun1399.com/",
  line_id: "[待 Hans 提供]",
  email: "[待 Hans 提供]",
  founded_year: 2025,
  preview_mode: true,
  noindex_all: true,
};

// 若於 Node / 模組環境使用
if (typeof module !== "undefined" && module.exports) {
  module.exports = SITE_CONFIG;
}
