<template>
  <div style="background-color: var(--lightest-grey)">    
    <h3 style="font-weight: bold;">
      Select quantitative data available on
      <span
        v-if="
          full_screen_note == 'All' ||
            full_screen_note[0] == -1 ||
            !full_screen_note
        "
      >
        all days</span
      >      
      <span
        v-if="
          full_screen_note != 'All' &&
            full_screen_note[0] != -1 &&
            full_screen_note
        "
      >
        <span style="font-size:small"
          >{{ full_screen_note[1].date_start.substring(0, 2) }}
          {{
            months[parseInt(full_screen_note[1].date_start.substring(3, 5)) - 1]
          }}
          {{ full_screen_note[1].date_start.substring(6, 10) }}
        </span>
      </span>
    </h3>
    <!-- display the available quantitative data values for selected day or display everything -->
    <div class="columns">
      <div class="column is-9">
        <div class="select">
          <select v-model="selected">
            <option v-bind:key="index" v-for="(name, index) in names_this_day">
              {{ name }}
            </option>
          </select>
        </div>
        <line-chart
          :chart-data="datacollection"
          :options="options"
        ></line-chart>
      </div>
      <!-- display note on the side if user pressed attached quantitative data button under a note text -->
      <div
        class="column scroll"
        v-if="
          full_screen_note != 'All' &&
            full_screen_note[0] != -1 &&
            full_screen_note
        "
        style="height: 87vh;"
      >
        <div>
          <h3 style="font-weight:bold">
            NOTE {{ full_screen_note[1].id + 1 }}:
            {{ full_screen_note[1].title }}
            <span style="font-size:small"
              >{{ full_screen_note[1].date_start.substring(0, 2) }}
              {{
                months[
                  parseInt(full_screen_note[1].date_start.substring(3, 5)) - 1
                ]
              }}
              {{ full_screen_note[1].date_start.substring(6, 10) }}
            </span>
          </h3>
        </div>

        <br />
        <p
          :id="'note_text' + full_screen_note[1].id"
          v-html="full_screen_note[1].text"
        ></p>
      </div>
    </div>
  </div>
</template>

<script>
import quant_data from "../assets/chartevents.json";
import LineChart from "../components/LineChart.js";

export default {
  name: "FullScreen",
  components: { LineChart },
  props: ["full_screen_note"], //[note_id, {note}]
  data() {
    return {
      quant_data: [], //all quantiative data
      name_one_occ: [], //all data with only one entry 
      name_multiple_occ: [], //data with more than 1 entry
      selected: "", //selected names for dropdown
      labels: [], //date labels on x-axis 
      months: [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
      ],
      names_this_day: [], //all data variables for day of the note 
      data_graph: [], //all quant values of one variable to display in graph
      datacollection: { //data for graph
        labels: [],
        datasets: [],
      },
      options: {}, //graph options
    };
  },
  methods: {
    //change data in graph if other variable is selected
    change_graph() {
      let data = this.quant_data.filter((data) => data.name == this.selected);
      console.log(data);
      let unit = "";
      if (data.length > 0 && data[0].unit != "None") {
        unit = data[0].unit;
      }
      let data_vals = [];
      this.labels = [];
      this.data_graph = [];
      for (let i = 0; i < data.length; i++) {
        data_vals.push([data[i].date, data[i].value]);
        this.labels.push(data[i].date);
        this.data_graph.push(parseInt(data[i].value));
      }
      console.log(data_vals);
      console.log(this.labels);
      console.log(this.data_graph);
      (this.datacollection = {
        labels: this.labels,
        datasets: [
          {
            label: this.selected + " " + unit,
            backgroundColor: "#2C7FB8",
            data: this.data_graph,
          },
        ],
      }),
        (this.options = {
          scales: {
            xAxes: [
              {
                type: "time",
                distribution: "series",
                time: {
                  parser: "DD/MM/YYYY HH:mm",
                  tooltipFormat: "ll HH:mm",
                  unit: "day",

                  displayFormats: {
                    day: "ll ",
                  },
                },
              },
            ],
          },
          legend: {
            display: true,
          },
          responsive: true,
          maintainAspectRatio: false,
        });
    },
  },
  watch: {
    //check if other data variable is selected
    selected() {
      this.change_graph();
    },
    //check if other attached quant data button is pressed or the quant data in the menu
    full_screen_note() {
      if (
        this.full_screen_note != "All" &&
        this.full_screen_note[0] != -1 &&
        this.full_screen_note
      ) {
        this.names_this_day = [];
        let day = this.full_screen_note[1].date_start;
        day = day.replaceAll("-", "/");
        day = day.substring(0, 10);
        for (let i = 0; i < this.name_multiple_occ.length; i++) {
          let filter = this.quant_data.filter(
            (data) => data.name == this.name_multiple_occ[i]
          );
          for (let j = 0; j < filter.length; j++) {
            if (
              filter[j].date.includes(day) &&
              !this.names_this_day.includes(this.name_multiple_occ[i])
            ) {
              this.names_this_day.push(this.name_multiple_occ[i]);
            }
            continue;
          }
        }
        console.log(this.names_this_day);
      } else {
        this.names_this_day = this.name_multiple_occ;
      }
    },
  },
  created() {
    this.quant_data = quant_data;
    let all_names = [];
    //get all data variable names
    for (let i = 0; i < this.quant_data.length; i++) {
      if (!all_names.includes(this.quant_data[i].name)) {
        all_names.push(this.quant_data[i].name);
      }
    }
    all_names.sort();
    //filter out all variables with only one value entry
    for (let i = 0; i < all_names.length; i++) {
      let tmp = this.quant_data.filter((data) => data.name == all_names[i]);
      if (tmp.length > 1) {
        this.name_multiple_occ.push(all_names[i]);
      } else {
        this.name_one_occ.push(all_names[i]);
      }
    }
  },
  mounted() {
    this.change_graph();
  },
};
</script>
