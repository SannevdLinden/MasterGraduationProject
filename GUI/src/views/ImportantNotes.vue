<template>
  <div class="about">
    <!-- quantitative data view-->
    <FullScreen
      class="overlay"
      v-bind:class="{ hidden: !full_screen_bool }"
      v-bind:full_screen_note="full_screen_note"
      v-on:full-screen-exit="full_screen_exit"
    />
    <!-- list with important notes/clusters of notes-->
    <div class="columns height_inherit">
      <div class="column is-12" style="padding-top:2rem; padding-left: 2rem;">
        <div class="columns height_90" id="container">
          <div class="column scroll" style="margin-top:0.75rem">
            <div class="columns">
              <div class="column">
                <div id="clusters_height">
                  <div
                    v-bind:key="index"
                    v-for="(cluster, index) in this.result"
                  >
                    <Cluster
                      v-bind:cluster="[
                        cluster,
                        clusterNoteButtons[index],
                        search_text,
                        search,
                        search_result,
                        true,
                        cluster_info_bookmarked_notes[index],
                      ]"
                      v-on:open-note="noteOpen"
                      v-on:highlight-word="highlight_words"
                      v-on:cluster-bookmark="bookmark_change"
                      v-on:open-note-alone="noteOpenAlone"
                      v-on:note-bookmark="bookmark_change_notes"
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>
          <!-- List with the note texts to display on the side-->
          <div class="column is-5" v-bind:class="{ hidden: !display_notes }">
            <button v-on:click="hideNotes" class="button button_style">
              Back
            </button>
            <NotesList
              v-bind:notes_id_display="[
                notes_id_display,
                search_text,
                search,
                search_result,
              ]"
              v-on:full-screen="full_screen"
              v-on:notes-bookmark="bookmark_change_notes"
              style="margin-top:0.5rem"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Cluster from "../components/Cluster.vue";
import NotesList from "../components/Notes.vue";
import FullScreen from "../components/FullScreen.vue";

export default {
  name: "ImportantNotes",
  props: ["data_to_child"],
  components: {
    Cluster,
    NotesList,
    FullScreen,
  },
  data() {
    return {
      clustersNotes: [], //all clusters 
      clusters_after_bookmark_filter: [], //make sure filtered notes only are local
      notes: [], //all notes
      clusterNoteButtons: [], //grey note buttons in the cluster 
      display_notes: false, //display notes on side
      notes_id_display: [], //[id note, [notes in this cluster], word for highlight] select notes to display on side and
      //which note button was pushed (id note)
      full_screen_bool: false, //display quant data view
      full_screen_note: [-1, { title: "", date: "", text: "" }], //which note should be displayed on the side in the quant data view 
      highlighted_word: "", //default highlighted word
      search_text: false, //if a search is executed
      search: "", //searched term
      search_result: "", //synonyms search
      bookmarked_notes: [], //bookmarks
      cluster_info_bookmarked_notes: [], //for every element in results [[cluster title, cluster dep, cluster data > if note else empty]]
      result: [], //all clusters of notes and notes to display in important note overview 
      prev_opened_clus: -1, //previous opened cluster to read the notes
      prev_note_cluster: -1, //previous opened note cluster (one single note) to read the notes
      prev_cluster: false, //if there is a previous cluster that was opened
    };
  },
  methods: {
    //open notes on the side and scroll the the note with id='id'
    noteOpen(id) {
      this.display_notes = true;
      // send only the notes that need to be displayed to NotesList component
      let notes_id_display = [id];
      let cluster_name = this.notes.Notes.filter((note) => note.id == id);
      cluster_name = cluster_name[0].cluster;
      let tmp = this.notes.Notes.filter((note) => note.cluster == cluster_name);
      notes_id_display.push(tmp);
      notes_id_display.push(this.highlighted_word);
      this.notes_id_display = notes_id_display;
      //change background color of opened previous cluster back and 
      //change color of currently opened cluster to darker background
      let cluster_id = this.clustersNotes.clusters.filter(
        (cluster) => cluster.name == cluster_name
      );
      if (
        (this.prev_note_cluster > -1 || this.prev_opened_clus > -1) &&
        (this.prev_opened_clus != cluster_id[0].id || !this.prev_cluster)
      ) {        
        if (this.prev_cluster) {
          const prev_elmnt = document.getElementById(
            "cluster_" + String(this.prev_opened_clus)
          );          
          if (prev_elmnt.style.backgroundColor == "var(--blue-opac-mid)") {
            prev_elmnt.style.backgroundColor = "var(--blue-opac)";
          } else if (
            prev_elmnt.style.backgroundColor == "var(--orange-opac-mid)"
          ) {
            prev_elmnt.style.backgroundColor = "var(--orange-opac)";
          }
        } else {
          const prev_elmnt = document.getElementById(
            "cluster_note_" + String(this.prev_note_cluster)
          );
          prev_elmnt.style.backgroundColor = "var(--grey-opac)";
        }
      }
      const elmnt = document.getElementById(
        "cluster_" + String(cluster_id[0].id)
      );
      if (elmnt.style.backgroundColor == "var(--blue-opac)") {
        elmnt.style.backgroundColor = "var(--blue-opac-mid)";
      } else if (elmnt.style.backgroundColor == "var(--orange-opac)") {
        elmnt.style.backgroundColor = "var(--orange-opac-mid)";
      }
      this.prev_opened_clus = cluster_id[0].id;
      this.prev_cluster = true;
      //scroll to the correct cluster and note
      if (elmnt) {
        setTimeout(() => elmnt.scrollIntoView(), 100);
      }
      setTimeout(() => this.scrollToNote(id), 100);
    },
    //scroll to the correct note
    scrollToNote(id) {
      const elmnt_note = document.getElementById(String(id));
      elmnt_note.scrollIntoView();
    },
    //open note on side for note cluster with note id='id'
    noteOpenAlone(id) {
      this.display_notes = true;
      // send only the notes that need to be displayed to NotesList component
      let notes_id_display = [id];
      let tmp = this.notes.Notes.filter((note) => note.id == id);
      notes_id_display.push(tmp);
      notes_id_display.push(this.highlighted_word);
      this.notes_id_display = notes_id_display;

      if (
        (this.prev_note_cluster > -1 || this.prev_opened_clus > -1) &&
        (this.prev_note_cluster != id || this.prev_cluster)
      ) {
        //change color of previous opened cluster/note and 
        //change background color current open cluster note
        if (this.prev_cluster) {
          const prev_elmnt = document.getElementById(
            "cluster_" + String(this.prev_opened_clus)
          );          
          if (prev_elmnt.style.backgroundColor == "var(--blue-opac-mid)") {
            prev_elmnt.style.backgroundColor = "var(--blue-opac)";
          } else if (
            prev_elmnt.style.backgroundColor == "var(--orange-opac-mid)"
          ) {
            prev_elmnt.style.backgroundColor = "var(--orange-opac)";
          }
        } else {
          const prev_elmnt = document.getElementById(
            "cluster_note_" + String(this.prev_note_cluster)
          );
          prev_elmnt.style.backgroundColor = "var(--grey-opac)";
        }
      }
      const elmnt = document.getElementById("cluster_note_" + String(id));
      elmnt.style.backgroundColor = "var(--grey-opac-mid)";
      this.prev_note_cluster = id;
      this.prev_cluster = false;
      //scroll to correct cluster
      if (elmnt) {
        setTimeout(() => elmnt.scrollIntoView(), 100);
      }
    },
    //hide the notes on the side
    hideNotes() {
      this.display_notes = false;
      if (this.prev_cluster) {
        const elmnt = document.getElementById(
          "cluster_" + String(this.prev_opened_clus)
        );
        if (elmnt) {
          setTimeout(() => elmnt.scrollIntoView(), 100);
        }
        const prev_elmnt = document.getElementById(
          "cluster_" + String(this.prev_opened_clus)
        );
        //change color last opened cluster back 
        if (prev_elmnt.style.backgroundColor == "var(--blue-opac-mid)") {
          prev_elmnt.style.backgroundColor = "var(--blue-opac)";
        } else if (
          prev_elmnt.style.backgroundColor == "var(--orange-opac-mid)"
        ) {
          prev_elmnt.style.backgroundColor = "var(--orange-opac)";
        } else if (prev_elmnt.style.backgroundColor == "var(--grey-opac-mid)") {
          prev_elmnt.style.backgroundColor = "var(--orange-opac)";
        }
      } else {
        //scroll to correct element
        const elmnt = document.getElementById(
          "cluster_note_" + String(this.prev_note_cluster)
        );
        if (elmnt) {
          setTimeout(() => elmnt.scrollIntoView(), 100);
        }
        const prev_elmnt = document.getElementById(
          "cluster_note_" + String(this.prev_note_cluster)
        );
        prev_elmnt.style.backgroundColor = "var(--grey-opac)";
      }
    },
    //open quant data view by pushing a attached quant data button with the note where id='id'
    full_screen(id) {
      console.log(this.full_screen_bool);      
      console.log("emit");
      this.$emit("full-screen-button", id);
    },
    //open quant data view via the top menu
    full_screen_menu(id) {
      console.log("id");
      console.log(id);
      this.full_screen_bool = true;
      this.full_screen_note = [];
      this.full_screen_note.push(id);
      if (id != "All") {
        let note = this.notes.Notes.filter((note) => note.id == id);
        this.full_screen_note.push(note[0]);
      }
    },
    //exit full screen
    full_screen_exit() {
      this.full_screen_bool = false;
    },
    //if user clicks on word in word summaries open or close the notes on the side
    highlight_words(word_info) {
      let id = word_info[1];
      let word = word_info[0];
      console.log(word);
      if (word_info[2] % 2 == 0) {
        this.highlighted_word = word;
        this.noteOpen(id);
      } else {
        this.highlighted_word = "";
        this.hideNotes();
        this.notes_id_display[2] = "";
      }
    },
    //emit that a bookmark of a cluster changed
    bookmark_change(data) {
      this.$emit("cluster-bookmark", data);
    },
    //emit that a bookmark of a note cluster changed
    bookmark_change_notes(data) {
      this.$emit("note-bookmark", data);
    },
    //filter for clusters with a bookmark that is true
    filter_bookmark() {
      this.clusters_after_bookmark_filter = this.clustersNotes.clusters;
      this.clusters_after_bookmark_filter = this.clusters_after_bookmark_filter.filter(
        (cluster) => cluster.bookmark == true
      );
    },
    //filter for note clusters with a bookmark that is true
    filter_bookmark_note() {
      this.bookmarked_notes = this.notes.Notes;
      this.bookmarked_notes = this.bookmarked_notes.filter(
        (note) => note.bookmark == true
      );
    },
    //combine the note cluster and clusters with a bookmark that is true to variable result in descending order
    combine_bookmarked() {
      let result = [];
      for (let i = 0; i < this.bookmarked_notes.length; i++) {
        result.push(this.bookmarked_notes[i]);
      }
      for (let i = 0; i < this.clusters_after_bookmark_filter.length; i++) {
        result.push(this.clusters_after_bookmark_filter[i]);
      }
      let time_a;
      let time_b;
      this.result = result.sort(function(a, b) {
        if (a.date_stop) {
          time_a = a.date_stop.split("-");
        } else {
          time_a = a.date_start.split("-");
        }
        if (b.date_stop) {
          time_b = b.date_stop.split("-");
        } else {
          time_b = b.date_start.split("-");
        }
        a = time_a;
        a = new Date(a[2], a[1] - 1, a[0]);
        a = a.getTime();
        b = time_b;
        b = new Date(b[2], b[1] - 1, b[0]);
        b = b.getTime();
        return b - a;
      });
      //get the cluster info for note clusters
      for (let i = 0; i < this.result.length; i++) {
        if (this.result[i].cluster) {
          let cluster_info = this.clustersNotes.clusters.filter(
            (cluster) => cluster.name == this.result[i].cluster
          );
          if (cluster_info.length > 0) {
            //with filtering notes this can be 0
            this.cluster_info_bookmarked_notes.push([
              cluster_info[0].id,
              cluster_info[0].title,
              cluster_info[0].department,
              cluster_info[0].date_start,
              cluster_info[0].date_stop,
            ]);
          }
        } else {
          this.cluster_info_bookmarked_notes.push([]);
        }
      }
    },
    //reverse the order of array based on the stop_date of the clusters or the date of the note
    //from newest to oldest
    reverse(data) {
      data.sort(function(a, b) {
        a = a.date_stop.split("-");
        a = new Date(a[2], a[1] - 1, a[0]);
        a = a.getTime();
        b = b.date_stop.split("-");
        b = new Date(b[2], b[1] - 1, b[0]);
        b = b.getTime();
        return b - a;
      });
      return data;
    },
  },
  created() {
    this.clustersNotes = this.data_to_child[1];
    this.notes = this.data_to_child[0];
    this.search_text = this.data_to_child[2];
    this.search = this.data_to_child[3];
    this.search_result = this.data_to_child[4];
    this.filter_bookmark();
    this.filter_bookmark_note();
    this.combine_bookmarked();
    console.log("UPDATE");
    console.log(this.result);
    console.log(this.clustersNotes);
    this.clusters_after_bookmark_filter = this.reverse(
      this.clusters_after_bookmark_filter
    );

    // to get the note button in the cluster boxes per cluster id
    // cluster.id ==0 is index 0 in clusterNoteButtons.
    // [[id note, date note, text], [id note, date note, text]] > per cluster
    //if is is a note the same is done with that note [[id note, date note, text]]
    let counter = 0;
    for (let i = 0; i < this.result.length; i++) {
      let results = [];
      if (this.result[i].date_stop) {
        let cluster_name = this.clusters_after_bookmark_filter[i - counter]
          .name;
        let tmp = this.notes.Notes.filter(
          (note) => note.cluster == cluster_name
        );
        for (let note of tmp) {
          results.push([note.id, note.date_start, note.text, note.title]);
        }
      } else {
        counter += 1;
        results = [
          [
            this.result[i].id,
            this.result[i].date_start,
            this.result[i].text,
            this.result[i].title,
          ],
        ];
      }

      this.clusterNoteButtons = [...this.clusterNoteButtons, results];
    }
  },
  mounted() {},
  watch: {
    data_to_child() {      
      this.clustersNotes = this.data_to_child[1];
      this.notes = this.data_to_child[0];
      this.search_text = this.data_to_child[2];
      this.search = this.data_to_child[3];
      this.search_result = this.data_to_child[4];
      this.filter_bookmark();
      this.filter_bookmark_note();
      this.combine_bookmarked();

      //check if all quantitative data or only the quant data attached to one note needs to be displayed
      if (this.data_to_child[7]) {
        if (this.data_to_child[8] == -1) {
          this.full_screen_menu("All");
        } else {
          this.full_screen_menu(this.data_to_child[8]);
        }
      } else {
        this.full_screen_exit();
      }
    },
  },
};
</script>

<style>
.full_height {
  height: 100vh;
}

.height_90 {
  height: 93vh;
}

.overlay {
  position: fixed;
  display: block;
  width: 75%;
  height: 100%;
  top: 0;
  left: 25%;
  right: 0;
  bottom: 0;
  background-color: rgba(255, 255, 255);
  z-index: 3;
  cursor: pointer;
}
.dot {
  height: 25px;
  width: 25px;
  background-color: #bbb;
  border-radius: 50%;
  display: block;
}

.vl5 {
  border-left: 5px solid #bbb;
  height: 25vh;
  margin-left: 10px;
}
.vl2 {
  border-left: 2px solid #bbb;
  height: 25vh;
  margin-left: 10px;
}
.vl1 {
  border-left: 1px solid #bbb;
  height: 25vh;
  margin-left: 10px;
}

.vl-dashed5 {
  border-left: 5px dashed #bbb;
  height: 25vh;
  margin-left: 10px;
}

.margin_left_30 {
  margin-left: 30%;
}

.margin-top-line {
  margin-top: -8px;
}

.margin-bottom-line {
  margin-bottom: 8px;
}
.margin-side-small5 {
  margin-left: 5px !important;
}
.margin-side-small2 {
  margin-left: 2px !important;
}
.margin-side-small1 {
  margin-left: 1px !important;
}

.small_vertical_bar {
  width: 2px;
  height: 10px;
  background-color: #bbb;
  margin-top: -2.5px;
}

.bar_to_cluster_stripe {
  height: 5px;
  background-color: #bbb;
}
</style>
