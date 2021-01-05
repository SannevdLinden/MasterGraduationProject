<template>
  <div id="app">
    <div class="columns height_inherit">
      <div class="column is-3"> <!-- left side panel with general and task info -->
        <div
          class="column is-full height_two_fifth border_side_bottom padding_normal"
        >
          <h2 class="header">General Patient Information</h2>
          <div class="scroll max_height_width">
            <GeneralPatientInfo />
          </div>
        </div>
        <div
          class="column is-full height_two_fifth border_side_bottom padding_normal"
        >
          <h2 class="header">Task Specific Information</h2>
          <div class="scroll max_height_width">
            <TaskSpecifcInfo />
          </div>
        </div>
      </div>

      <!-- panel with search and filter options -->
      <div class="column is-2" style="width:13% !important; padding-top:4rem;">
        <!-- search bar, reset and submit button -->
        <form>
          <input
            class="input"
            type="text"
            placeholder="Search"
            v-model="search_tmp"
            v-on:keyup.enter="search_term"
          />
          <input
            type="reset"
            value="Reset"
            v-on:click="remove_search"
            class="button button_style"
            style="padding-top:4px;"
          />
          <button
            v-on:click="search_term"
            class="button button_style"
            style="margin-left:0.5rem"
          >
            Submit
          </button>
        </form>
        <!-- box displaying the synonyms of searched term -->
        <div
          v-bind:class="{ hidden: !display_search_words }"
          style="margin-top:1rem;"
        >
          <h3 class="sub_header">Included in search:</h3>
          <div
            class="scroll"
            style="height: 20vh; border: 2px solid var(--dark-grey); border-radius: 8px;"
          >
            <div v-if="search_result == 'no results'" style="padding: 0.5rem;">
              No synonyms were found
            </div>
            <div v-else style="padding: 0.5rem;">
              <div
                v-for="(term, index) in search_result"
                :id="'search_term' + index"
                v-bind:key="index"
              >
                <span v-if="index == 0">{{ search }} <br /></span>
                <div
                  v-if="index % 2 == 0"
                  style="background-color:var(--grey); border-radius: 8px;"
                >
                  <span style="padding: 0.2rem; display:block; hyphens: auto;">
                    {{ term }}</span
                  >
                </div>
                <div v-if="index % 2 != 0">
                  <span style="padding: 0.2rem; display:block; hyphens: auto;"
                    >{{ term }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- specialism filters -->
        <h3 class="sub_header">Specialism:</h3>
        <div v-for="depart in departments" v-bind:key="depart">
          <label class="is-checkbox">
            <input
              id="mycheckbox"
              checked="checked"
              type="checkbox"
              v-bind:value="depart"
              v-model="checkedBoxesSpecialism"
              v-on:change="filterNotes('Specialism', depart)"
            />
            <span class="icon checkmark">
              <font-awesome-icon :icon="['fas', 'check']" />
            </span>
            <span>{{ depart }}</span>
          </label>
          <br />
        </div>

        <!-- cluster type filters -->
        <h3 class="sub_header">Cluster type:</h3>
        <div style="width:100%; opacity: 0.4;">
          <label class="is-checkbox">
            <input id="mycheckbox" type="checkbox" disabled />
            <span class="icon checkmark is-red" style="margin-top: 0.5rem;">
              <font-awesome-icon
                class="red-background"
                :icon="['fas', 'check']"
              />
            </span>
            <span
              >ER without <br />
              hospitalization</span
            >
          </label>
        </div>

        <label class="is-checkbox">
          <input
            id="mycheckbox"
            checked="checked"
            type="checkbox"
            v-bind:value="'Check-ups'"
            v-model="checkedBoxesType"
            v-on:change="filterNotes('Type', 'Check-ups')"
          />
          <span class="icon checkmark is-blue">
            <font-awesome-icon
              class="blue-background"
              :icon="['fas', 'check']"
            />
          </span>
          <span>Check-ups</span>
        </label>

        <div style="width:100%; opacity: 0.4;">
          <label class="is-checkbox">
            <input id="mycheckbox" type="checkbox" disabled />
            <span class="icon checkmark is-green" style="margin-top: 0.5rem;">
              <font-awesome-icon
                class="green-background"
                :icon="['fas', 'check']"
              />
            </span>
            <span
              >Small <br />
              interventions</span
            >
          </label>
        </div>

        <label class="is-checkbox">
          <input
            id="mycheckbox"
            checked="checked"
            type="checkbox"
            v-bind:value="'Admission'"
            v-model="checkedBoxesType"
            v-on:change="filterNotes('Type', 'Admission')"
          />
          <span class="icon checkmark is-orange" style="margin-top: 0.5rem;">
            <font-awesome-icon
              class="orange-background"
              :icon="['fas', 'check']"
            />
          </span>
          <span
            >Hospital <br />
            admissions</span
          >
        </label>        
      </div>

      <!-- main panel with the navigation on top and either the medical
      history or important note overview views -->
      <div class="column">
        <Navigation
          v-on:open-quant-data="quant_data_func"
          v-on:close-quant-data="quant_data_func_close"
          v-bind:full_screen_but="[full_screen_but]"
        />
        <router-view
          v-bind:data_to_child="[
            notes_to_child,
            clustersNotes_to_child,
            search_text,
            search,
            search_result,
            display_notes,
            note_id_to_display,
            quant_data,
            quant_data_id,
          ]"
          :key="data_changed"
          v-on:cluster-bookmark="bookmark_change"
          v-on:note-bookmark="bookmark_change_notes"
          v-on:full-screen-button="full_screen_button"
        />
      </div>
    </div>
  </div>
</template>

<script>
import GeneralPatientInfo from "./components/GeneralPatientInfo";
import TaskSpecifcInfo from "./components/TaskSpecificInfo";
import Navigation from "./components/Navigation";
import clusters from "./assets/clusters.json";
import Notes from "./assets/Notes.json";
import axios from "axios";

export default {
  name: "app",
  components: {
    GeneralPatientInfo,
    TaskSpecifcInfo,
    Navigation,
  },
  data() {
    return {
      clustersNotes: [], //all clusters
      notes: [], // all notes
      notes_to_child: [], // notes to pass to the views
      clustersNotes_to_child: [], //clusters to pass to the views
      departments: [], // all departments present
      checkedBoxesSpecialism: [], // which check boxes are checked in specialism filter
      checkedBoxesType: ["Check-ups", "Admission"], //check box types for cluster type filter
      data_changed: 0, //number changes if something changes 
      search: "", // search term
      search_result: "", //search result
      display_search_words: false, //if the synonyms box should be displayed
      search_text: false, //if the yellow marking should be displayed
      search_tmp: "", //temporary place holder searched terms directly from search bar
      display_notes: false, //display the notes on the side
      note_id_to_display: -1, //which notes should be displayed on the side
      remove_cluster: [], //clusters that are removed due to filtering
      quant_data: false, //display quant data view
      quant_data_id: -1, //which note should be displayed next to the quant data
      full_screen_but: 0, //if the quant data should be displayed on full screen
    };
  },
  methods: {
    //filtering the notes based on specialism or/and cluster type
    //filter_type is either specialism of cluster type
    //removed is which option should be removed, e.g. Check-ups
    filterNotes(filter_type, removed) {
      let tmp = [];
      if (filter_type == "Specialism") {
        //filter notes based on specialisms
        for (let i = 0; i < this.checkedBoxesSpecialism.length; i++) {
          let result = this.notes.Notes.filter((note) =>
            note.department.includes(this.checkedBoxesSpecialism[i])
          );
          for (let x of result) {
            tmp.push(x);
          }
        }
        this.notes_to_child = { Notes: tmp };
        //check if a cluster (dis)appears due to filtering > if cluster only has the filtered department(s)
        let filtered_out_dep = this.departments.filter(
          (value) => !this.checkedBoxesSpecialism.includes(value)
        );
        if (this.clustersNotes.clusters.length) {
          //find cluster id that needs to be removed or added
          for (let i = 0; i < this.clustersNotes.clusters.length; i++) {
            //if cluster contains only one department and that is part of the removed departments
            if (this.clustersNotes.clusters[i].department.length == 1) {
              if (
                this.clustersNotes.clusters[i].department[0] == removed &&
                !this.remove_cluster.includes(this.clustersNotes.clusters[i].id)
              ) {
                this.remove_cluster.push(this.clustersNotes.clusters[i].id);
              }
            }
            //if cluster is removed due to a combination of filtered out deparments
            if (
              this.clustersNotes.clusters[i].department.length <=
              filtered_out_dep.length
            ) {
              let push_to_remove = true;
              for (
                let j = 0;
                j < this.clustersNotes.clusters[i].department.length;
                j++
              ) {
                if (
                  !filtered_out_dep.includes(
                    this.clustersNotes.clusters[i].department[j]
                  )
                ) {
                  push_to_remove = false;
                }
              }
              if (
                push_to_remove &&
                !this.remove_cluster.includes(this.clustersNotes.clusters[i].id)
              ) {
                this.remove_cluster.push(this.clustersNotes.clusters[i].id);
              }
            }
          }
          if (
            this.remove_cluster.length > 0 &&
            this.checkedBoxesSpecialism.includes(removed) == false
          ) {
            //remove them
            for (let i = 0; i < this.remove_cluster.length; i++) {
              let tmp_filter = this.clustersNotes_to_child.clusters.filter(
                (cluster) => cluster.id != this.remove_cluster[i]
              );
              this.clustersNotes_to_child = { clusters: tmp_filter };
            }
          } else if (this.remove_cluster.length > 0) {
            //add a cluster
            let added_ids = [];
            for (let i = 0; i < this.remove_cluster.length; i++) {
              let push_to_add = false;
              let cluster_to_check = this.clustersNotes.clusters.filter(
                (cluster) => cluster.id == this.remove_cluster[i]
              ); //gives array back with one cluster in it
              for (let j = 0; j < cluster_to_check[0].department.length; j++) {
                if (
                  this.checkedBoxesSpecialism.includes(
                    cluster_to_check[0].department[j]
                  )
                ) {
                  push_to_add = true;
                  break;
                }
              }
              if (push_to_add) {
                this.clustersNotes_to_child.clusters.push(cluster_to_check[0]);
                added_ids.push(cluster_to_check[0].id);
              }
            }
            this.remove_cluster = this.remove_cluster.filter(
              (value) => !added_ids.includes(value)
            );
          }
        }
      } else if (filter_type == "Type") {
        //filter based on cluster type
        for (let i = 0; i < this.checkedBoxesType.length; i++) {
          let result = this.clustersNotes.clusters.filter(
            (cluster) => cluster.title == this.checkedBoxesType[i]
          );
          for (let x of result) {
            tmp.push(x);
          }
        }
        this.clustersNotes_to_child = { clusters: tmp };
        // also check specialism filters 
        this.filterNotes("Specialism");
      }
      this.data_changed += 1; //data changed so push to children (different views)
      if (this.clustersNotes_to_child.clusters) {
        //sort the cluster data
        this.clustersNotes_to_child.clusters.sort(function(a, b) {
          return a.id - b.id;
        });
      }
      if (this.notes_to_child.Notes) {
        //sort the note data
        this.notes_to_child.Notes.sort(function(a, b) {
          return a.id - b.id;
        });
      }
    },
    //search for terms
    search_term() {
      console.log(this.search_tmp);
      //reset the previous search
      this.search = "";
      this.search_text = true;
      this.search_result = "no results";
      //post to flask and handle response
      axios
        .post("http://127.0.0.1:5000/", {
          search: this.search_tmp,
        })
        .then((response) => {
          this.search_result = response.data.search_result;
          console.log("SEARCH");
          console.log(this.search_result);
          if (this.search_result != "no results") {
            this.search_result.sort();
          }
          console.log(this.search_result);
          this.display_search_words = true;
          this.search_text = true;
          this.search = this.search_tmp;
        });
    },
    //reset search
    remove_search() {
      this.search_text = false;
      this.search = "";
      this.display_search_words = false;
    },
    //change in a bookmark for a cluster
    //data = [cluster_id, bool with bookmark status]
    bookmark_change(data) {
      let cluster_id = data[0];
      let bookmark = data[1];
      console.log("bookmark");
      console.log(cluster_id);
      console.log(bookmark);
      //change bookmark in data
      for (let i = 0; i < this.clustersNotes.clusters.length; i++) {
        if (this.clustersNotes.clusters[i].id == cluster_id) {
          this.clustersNotes.clusters[i].bookmark = bookmark;
        }
      }
      for (let i = 0; i < this.clustersNotes_to_child.clusters.length; i++) {
        if (this.clustersNotes_to_child.clusters[i].id == cluster_id) {
          this.clustersNotes_to_child.clusters[i].bookmark = bookmark;
        }
      }
      //push this new data to children
      this.data_changed += 1;
    },
    //change in a bookmark for a note
    //data = [note_id, bool with bookmark status]
    bookmark_change_notes(data) {
      let note_id = data[0];
      let bookmark = data[1];
      this.display_notes = true;
      this.note_id_to_display = note_id;
      console.log("bookmark note");
      console.log(note_id);
      console.log(bookmark);
      //change bookmark in data
      for (let i = 0; i < this.notes.Notes.length; i++) {
        if (this.notes.Notes[i].id == note_id) {
          this.notes.Notes[i].bookmark = bookmark;
        }
      }
      for (let i = 0; i < this.notes_to_child.Notes.length; i++) {
        if (this.notes_to_child.Notes[i].id == note_id) {
          this.notes_to_child.Notes[i].bookmark = bookmark;
        }
      }
      //push this new data to children
      this.data_changed += 1;
    },
    //open quantitative data view via menu
    quant_data_func() {
      this.quant_data = true;
    },
    //close quantitative data view via menu
    quant_data_func_close() {
      this.quant_data = false;
      this.quant_data_id = -1;
    },
    //open quantitative data view by clicking on attached quant data button
    //id is the note to open on the side of the quantitative data
    full_screen_button(id) {
      this.quant_data_func();
      this.full_screen_but += 1;
      this.quant_data_id = id;
    },
  },
  created() {
    this.clustersNotes = clusters;
    this.notes = Notes;
    //get all the different departments in the notes
    let departments = new Set();
    for (let note of this.notes.Notes) {
      for (let department of note.department) {
        departments.add(department);
      }
    }
    this.departments = Array.from(departments);
    this.checkedBoxesSpecialism = this.departments;
    this.filterNotes("Specialism"); // fill filtered note array on creation
    this.filterNotes("Type");
  },
};
</script>

<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background-color: var(--lightest-grey);
  height: 100vh;
}
.hidden {
  display: none !important;
}

.border_side_bottom {
  border-style: none solid solid none;
  border-width: thin;
  border-color: #474745; //To Do make general color sheet
}

#nav {
  padding-top: 1rem;
  padding-left: 1rem;

  a {
    font-weight: bold;
    color: var(--darkest-grey);

    &.router-link-exact-active {
      color: var(--grey);
    }
  }
}

.height_inherit {
  height: inherit;
}

.height_two_fifth {
  height: 50vh;
}

.height_one_fifth {
  height: 20vh;
}

.scroll {
  overflow-y: scroll;
}

.scroll::-webkit-scrollbar {
  -webkit-appearance: none;
}

.scroll::-webkit-scrollbar:vertical {
  width: 11px;
}

.scroll::-webkit-scrollbar:horizontal {
  height: 11px;
}

.scroll::-webkit-scrollbar-thumb {
  border-radius: 8px;
  border: 2px solid var(--lightest-grey); /* should match background, can't be transparent */
  background-color: var(--dark-grey);
}

.padding_normal {
  padding: 1rem 0.5rem 1rem 1.75rem !important;
}

.max_height_width {
  height: 90%;
  width: 100%;
}

.header {
  color: var(--darkest-grey);
  font-size: large;
  font-weight: bold;
}

.bold {
  font-weight: bold;
}

.display_flex {
  display: flex;
}

.margin_left_normal {
  margin-left: 1rem;
}

.table_padding_left {
  padding-left: 0.5rem;
}

th {
  font-weight: normal;
}

.input {
  border-color: var(--darkest-grey) !important;
  color: var(--dark-grey) !important;
  border-radius: 8px !important;
}

.button_style {
  background-color: var(--dark-grey) !important;
  color: var(--lightest-grey) !important;
  border-radius: 12px !important;
  border: none !important;
  height: 2em !important;
  margin-top: 0.5rem !important;
}

.button_note {
  width: 80px;
}

.sub_header {
  font-size: large !important;
  margin-top: 1rem !important;
}

label.is-checkbox {
  border: none;
  color: var(--darkest-grey);
  white-space: nowrap;
  display: inline-flex;
  justify-content: center;
  margin-top: 0.5rem;

  cursor: pointer;
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;

  .checkmark {
    color: transparent;
    position: relative;
    i {
      z-index: 1;
    }
    &:before {
      content: "";
      position: absolute;
      right: 0;
      left: 0;
      top: 0;
      bottom: 0;
      z-index: 0;
      border-radius: 8px;
      border: 3px solid var(--grey);
    }
  }
  .is-blue {
    &:before {
      border: 3px solid var(--blue) !important;
    }
  }
  .is-red {
    &:before {
      border: 3px solid var(--red) !important;
    }
  }
  .is-orange {
    &:before {
      border: 3px solid var(--orange) !important;
    }
  }
  .is-green {
    &:before {
      border: 3px solid var(--green-button) !important;
    }
  }
  input[type="checkbox"] {
    position: absolute;
    visibility: hidden;
    cursor: pointer;
    &:checked ~ .checkmark {
      color: var(--lightest-grey);
      background-color: var(--grey);
      border-radius: 8px;
      .blue-background {
        background-color: var(--blue) !important;
        border-radius: 8px;
        color: var(--lightest-grey);
      }
      .red-background {
        background-color: var(--red) !important;
        border-radius: 8px;
        color: var(--lightest-grey);
      }
      .orange-background {
        background-color: var(--orange) !important;
        border-radius: 8px;
        color: var(--lightest-grey);
      }
      .green-background {
        background-color: var(--green) !important;
        border-radius: 8px;
        color: var(--lightest-grey);
      }
    }
  }
  .svg-inline--fa.fa-w-16 {
    width: 1.5em;
  }
  .svg-inline--fa {
    height: 1.2em;
  }
  .icon {
    & {
      height: 1.5em;
      width: 1.5em;
      margin-right: 0.35em;
    }
  }
}
</style>
