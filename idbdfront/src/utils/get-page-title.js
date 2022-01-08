import defaultSettings from '@/settings'

const title = defaultSettings.title || '驾驶员违规驾驶行为监测系统'

export default function getPageTitle(pageTitle) {
  if (pageTitle) {
    return `${pageTitle} - ${title}`
  }
  return `${title}`
}
