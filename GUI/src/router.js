import Vue from 'vue'
import Router from 'vue-router'
import ImportantNotes from './views/ImportantNotes.vue'
import MedicalHistory from './views/MedicalHistory.vue'

Vue.use(Router)

export default new Router({
    routes: [
        {
            path: '/',
            name: 'ImportantNotes',
            component: ImportantNotes
        }, 
        {
            path: '/MedicalHistory',
            name: 'MedicalHistory',
            component: MedicalHistory
        }
    ]
})