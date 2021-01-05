import Vue from 'vue'
import App from './App.vue'
import router from './router'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faStar as faStarReg} from '@fortawesome/free-regular-svg-icons'
import { faStar as faStarOpen} from '@fortawesome/free-solid-svg-icons'
import {faAngleRight} from '@fortawesome/free-solid-svg-icons'
import {faCheck} from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import './assets/main.scss';
import VueFusionCharts from 'vue-fusioncharts';
import FusionCharts from 'fusioncharts';
import TimeSeries from 'fusioncharts/fusioncharts.timeseries';
//import the theme
import FusionTheme from 'fusioncharts/themes/fusioncharts.theme.fusion';

library.add(faStarReg, faStarOpen, faAngleRight, faCheck)

Vue.component('font-awesome-icon', FontAwesomeIcon)
Vue.use(require('vue-moment'), VueFusionCharts, FusionCharts, TimeSeries, FusionTheme);

Vue.config.productionTip = false

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
