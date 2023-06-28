<template>
  <div class="font_size_small">
    <!-- display all task specific information-->
    <table style="table-layout: auto; width: 100%;" v-if="task_admis">
      <tr>
        <th class="bold">Admission:</th>
        <th class="table_padding_left">
          {{ data.generalPatientInfo.admission }}
        </th>
      </tr>
      <tr>
        <th class="bold">Admission Diagnosis:</th>
        <th class="table_padding_left">
          {{ data.generalPatientInfo.admission_diagnosis }}
        </th>
      </tr>
      <tr>
        <th class="bold">Admission Treatment:</th>
        <th class="table_padding_left">
          {{ data.generalPatientInfo.current_treatment }}
        </th>
      </tr>
      <tr>
        <th class="bold">Medication on Admission:</th>
        <th class="table_padding_left">
          {{ data.generalPatientInfo.medication_admission }}
        </th>
      </tr>
    </table>

    <table style="table-layout: auto; width: 100%;" v-if="!task_admis">
      <tr>
        <th class="bold">Latest Admission:</th>
        <th class="table_padding_left">
          {{ data.generalPatientInfo.latest_admission }}
        </th>
      </tr>
      <tr>
        <th class="bold">Discharge Location:</th>
        <th class="table_padding_left">
          {{ data.generalPatientInfo.discharge_location }}
        </th>
      </tr>
      <tr>
        <th class="bold">Discharge Diagnosis:</th>
        <th class="table_padding_left">
          {{ data.generalPatientInfo.discharge_diagnosis }}
        </th>
      </tr>
      <tr>
        <th class="bold">Medication Discharge:</th>
        <th class="table_padding_left">
          {{ data.generalPatientInfo.medication_discharge }}
        </th>
      </tr>
      <tr>
        <th class="bold">Latest Check-up:</th>
        <th class="table_padding_left">
          {{ data.generalPatientInfo.lastest_checkup }}
        </th>
      </tr>
    </table>
  </div>
</template>

<script>
import generalPatientInfo from "../assets/generalPatientInfo.json";

export default {
  name: "TaskSpecificInfo",
  data() {
    return {
      data: [],
      task_admis: false, //if it is an long term check-up or check while patient is admitted task
    };
  },
  created() {
    this.data = generalPatientInfo;
    console.log(this.data.generalPatientInfo.name);
  },
};
</script>

<style scoped>
.font_size_small {
  font-size: 14px;
}
</style>
