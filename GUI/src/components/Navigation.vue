<template>
  <div>
    <div id="nav">
      <router-link
        to="/"
        class="header"
        @click.native="openImportant"
        :style="important_background"
        >Important Note Overview</router-link
      >
      |
      <router-link
        to="/MedicalHistory"
        @click.native="openHis"
        class="header"
        :style="medical_background"
        >Medical History</router-link
      >
      |
      <span
        class="header"
        v-on:click="openQuant"
        :style="quant_background"
        style="cursor: pointer;"
        >Quantitative Data</span
      >
    </div>
  </div>
</template>

<script>
export default {
  name: "Navigation",
  props: ["full_screen_but"], //check if the quantitative data view needs to be opened
  data() {
    return {
      //background colors for selected and non selected headers in menu
      important_background: { 
        color: "var(--grey) !important",
      },
      medical_background: {
        color: "var(--darkest-grey) !important",
      },
      quant_background: {
        color: "var(--darkest-grey) !important",
      },
      med_color: false, //check if this page is shown
      important_color: false, //check if this page is shown
      prev_button_num: 0, //which view was previously opened 
    };
  },
  methods: {
    //open quantitative data view
    openQuant() {
      this.$emit("open-quant-data");
      this.important_background.color = "var(--darkest-grey) !important";
      this.medical_background.color = "var(--darkest-grey) !important";
      this.quant_background.color = "var(--grey) !important";
      this.med_color = false;
      this.important_color = false;
    },
    //open medical history view
    openHis() {
      this.$emit("close-quant-data");
      this.important_background.color = "var(--darkest-grey) !important";
      this.medical_background.color = "var(--grey) !important";
      this.quant_background.color = "var(--darkest-grey) !important";
      this.med_color = true;
      this.important_color = false;
      console.log("open his");
      console.log(this.quant_background);
    },
    //open important note overview view
    openImportant() {
      this.$emit("close-quant-data");
      this.important_background.color = "var(--grey) !important";
      this.medical_background.color = "var(--darkest-grey) !important";
      this.quant_background.color = "var(--darkest-grey) !important";
      this.med_color = false;
      this.important_color = true;
      console.log("open important");
      console.log(this.quant_background);
    },
  },
  watch: {
    //check if quant data view is opened by clicking on attached quant data button
    full_screen_but() {
      console.log("full screen but");
      console.log(this.full_screen_but);
      console.log(this.prev_button_num);
      if (this.prev_button_num != this.full_screen_but[0]) {
        console.log("color change");
        this.important_background.color = "var(--darkest-grey) !important";
        this.medical_background.color = "var(--darkest-grey) !important";
        this.quant_background.color = "var(--grey) !important";
        this.prev_button_num = this.full_screen_but[0];
      }
    },
  },
};
</script>

<style scoped>
hr {
  width: 25%;
  background-color: var(--darkest-grey);
  margin: 0.75rem 37.5%;
}
</style>
