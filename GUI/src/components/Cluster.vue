<template>
  <div class="display_flex">
    <!-- horizontal bar connecting cluster to timeline-->
    <div
      class="bar_to_cluster_stripe"
      :style="stripe_background"
      style="width:5%; margin-top:25px;"
      :id="'cluster_stripe' + cluster[0].id"
      v-if="!cluster[5]"
    ></div>
    <!-- cluster summary box -->
    <div
      class="cluster_box"
      :style="cluster_background"
      :id="'cluster_' + cluster[0].id"
      v-if="cluster[0].date_stop"
      style="width:100%;"
    >
      <div style="padding:1rem;">
        <div class="display_flex" style="justify-content: space-between;">
          <div>
            <span style="font-weight: bold;"
              >CLUSTER: {{ cluster[0].title }}:
            </span>
            <span
              v-for="(dep, ind) in cluster[0].department"
              v-bind:key="ind"
              style="font-weight: bold;"
              >{{ dep }},
            </span>
            <span
              style="font-weight: bold; font-size:small"
              v-if="cluster[0].date_stop != cluster[0].date_start"
            >
              {{ cluster[0].date_start.substring(0, 2) }}
              {{ months[parseInt(cluster[0].date_start.substring(3, 5)) - 1] }}
              {{ cluster[0].date_start.substring(6, 10) }} till
              {{ cluster[0].date_stop.substring(0, 2) }}
              {{ months[parseInt(cluster[0].date_stop.substring(3, 5)) - 1] }}
              {{ cluster[0].date_stop.substring(6, 10) }}</span
            >
            <span
              style="font-weight: bold; font-size:small"
              v-if="cluster[0].date_stop == cluster[0].date_start"
            >
              {{ cluster[0].date_start.substring(0, 2) }}
              {{ months[parseInt(cluster[0].date_start.substring(3, 5)) - 1] }}
              {{ cluster[0].date_start.substring(6, 10) }}
            </span>
          </div>
          <div style="padding-left: 0.5rem;" :style="cluster_color">
            <span v-if="bookmark == false" v-on:click="bookmark_change">
              <font-awesome-icon :icon="['far', 'star']" />
            </span>
            <span v-if="bookmark == true" v-on:click="bookmark_change">
              <font-awesome-icon :icon="['fas', 'star']" />
              <!-- far/fas star -->
            </span>
          </div>
        </div>
        <!-- summary words-->
        <div style="margin-top: 0.5rem">
        <!-- for fabian's concept space summary version use this code-->
          <div v-if="fabians_version">
            <div v-if="concept_space_data.disease.length > 0">
              <span style="font-weight: bold;">Diseases:</span>
              <span
                v-for="(word, index) in concept_space_data.disease"
                v-bind:key="index"
              >
                <span
                  v-if="index != concept_space_data.disease.length - 1"
                  :id="'word_' + word[0].toLowerCase()"
                  v-on:click="highlight_word([word[0], word[1]])"
                >
                  {{ word[0] }}</span
                >
                <span v-if="index != concept_space_data.disease.length - 1"
                  >,</span
                >
                <span
                  v-if="index == concept_space_data.disease.length - 1"
                  :id="'word_' + word[0].toLowerCase()"
                  v-on:click="highlight_word([word[0], word[1]])"
                >
                  {{ word[0] }}</span
                >
              </span>
            </div>
          </div>
          <!-- summary disease words -->
          <div v-if="!fabians_version">
            <div v-if="cluster[0].disease_words.length > 0">
              <span style="font-weight: bold;">Diseases:</span>
              <span
                v-for="(word, index) in cluster[0].disease_words"
                v-bind:key="index"
              >
                <span
                  v-if="index != cluster[0].disease_words.length - 1"
                  :id="'word_' + word.toLowerCase()"
                  v-on:click="highlight_word(word)"
                >
                  {{ word }}</span
                >
                <span v-if="index != cluster[0].disease_words.length - 1"
                  >,</span
                >
                <span
                  v-if="index == cluster[0].disease_words.length - 1"
                  :id="'word_' + word.toLowerCase()"
                  v-on:click="highlight_word(word)"
                >
                  {{ word }}</span
                >
              </span>
            </div>
          </div>
          <!-- for fabian's concept space summary version use this code-->
          <div v-if="fabians_version">
            <div v-if="concept_space_data.drug.length > 0">
              <span style="font-weight: bold;">Drugs:</span>
              <span
                v-for="(word, index) in concept_space_data.drug"
                v-bind:key="index"
              >
                <span
                  v-if="index != concept_space_data.drug.length - 1"
                  :id="'word_' + word[0].toLowerCase()"
                  v-on:click="highlight_word([word[0], word[1]])"
                >
                  {{ word[0] }}</span
                >
                <span v-if="index != concept_space_data.drug.length - 1"
                  >,</span
                >
                <span
                  v-if="index == concept_space_data.drug.length - 1"
                  :id="'word_' + word[0].toLowerCase()"
                  v-on:click="highlight_word([word[0], word[1]])"
                >
                  {{ word[0] }}</span
                >
              </span>
            </div>
          </div>
          <!-- drugs summary words-->
          <div v-if="!fabians_version">
            <div v-if="cluster[0].drugs_words.length > 0">
              <span style="font-weight: bold;">Drugs:</span>
              <span
                v-for="(word, index) in cluster[0].drugs_words"
                v-bind:key="index"
              >
                <span
                  v-if="index != cluster[0].drugs_words.length - 1"
                  :id="'word_' + word.toLowerCase()"
                  v-on:click="highlight_word(word)"
                >
                  {{ word }}</span
                >
                <span v-if="index != cluster[0].drugs_words.length - 1">,</span>
                <span
                  v-if="index == cluster[0].drugs_words.length - 1"
                  :id="'word_' + word.toLowerCase()"
                  v-on:click="highlight_word(word)"
                >
                  {{ word }}</span
                >
              </span>
            </div>
          </div>
          <!-- for fabian's concept space summary version use this code-->
          <div v-if="fabians_version">
            <div v-if="concept_space_data.procedure.length > 0">
              <span style="font-weight: bold;">Procedures:</span>
              <span
                v-for="(word, index) in concept_space_data.procedure"
                v-bind:key="index"
              >
                <span
                  v-if="index != concept_space_data.procedure.length - 1"
                  :id="'word_' + word[0].toLowerCase()"
                  v-on:click="highlight_word([word[0], word[1]])"
                >
                  {{ word[0] }}</span
                >
                <span v-if="index != concept_space_data.procedure.length - 1"
                  >,</span
                >
                <span
                  v-if="index == concept_space_data.procedure.length - 1"
                  :id="'word_' + word[0].toLowerCase()"
                  v-on:click="highlight_word([word[0], word[1]])"
                >
                  {{ word[0] }}</span
                >
              </span>
            </div>
          </div>
          <!-- summary procedure words-->
          <div v-if="!fabians_version">
            <div v-if="cluster[0].procedure_words.length > 0">
              <span style="font-weight: bold;">Procedures:</span>
              <span
                v-for="(word, index) in cluster[0].procedure_words"
                v-bind:key="index"
              >
                <span
                  v-if="index != cluster[0].procedure_words.length - 1"
                  :id="'word_' + word.toLowerCase()"
                  v-on:click="highlight_word(word)"
                >
                  {{ word }}</span
                >
                <span v-if="index != cluster[0].procedure_words.length - 1"
                  >,</span
                >
                <span
                  v-if="index == cluster[0].procedure_words.length - 1"
                  :id="'word_' + word.toLowerCase()"
                  v-on:click="highlight_word(word)"
                >
                  {{ word }}</span
                >
              </span>
            </div>
          </div>
          <!-- note buttons-->
          <div>
            <h4 style="font-weight: bold;">Notes:</h4>
            <div class="buttons">
              <div
                v-for="(note, ind) in cluster[1].slice().reverse()"
                v-bind:key="ind"
              >
                <div
                  v-if="search_previews[cluster[1].length - 1 - ind]"
                  class="tooltip"
                  :id="'button_' + note[0]"
                >
                  <button
                    v-if="
                      search_previews[cluster[1].length - 1 - ind].length > 0
                    "
                    v-on:click="open_note(note[0])"
                    class="button button_style button_note"
                    style="margin-right: 0.5rem; background-color: #F6BE00 !important; color:var(--darkest-grey) !important; 
                                        border: 2px solid !important;"
                  >
                    {{ note[0] + 1 }}. {{ note[3].substring(0, 3) }}
                  </button>

                  <div
                    v-if="
                      search_previews[cluster[1].length - 1 - ind].length > 0
                    "
                    class="tooltiptext"
                    :id="'snippet_' + note[0]"
                  >
                    <p
                      v-for="(snippet, i) in search_previews[
                        cluster[1].length - 1 - ind
                      ]"
                      v-bind:key="i"
                    >
                      ... {{ snippet }} ...
                    </p>
                    <span
                      class="tooltip_arrow"
                      :id="'snippet_arrow_' + note[0]"
                    ></span>
                  </div>

                  <button
                    v-if="
                      !search_previews[cluster[1].length - 1 - ind].length > 0
                    "
                    v-on:click="open_note(note[0])"
                    class="button button_style button_note"
                    style="margin-right: 0.5rem;"
                  >
                    {{ note[0] + 1 }}. {{ note[3].substring(0, 3) }}
                  </button>
                </div>
                <div
                  v-if="!search_previews[cluster[1].length - 1 - ind]"
                  :id="'button_' + note[0]"
                >
                  <button
                    v-if="!search_previews[cluster[1].length - 1 - ind]"
                    v-on:click="open_note(note[0])"
                    class="button button_style button_note"
                    style="margin-right: 0.5rem;"
                  >
                    {{ note[0] + 1 }}. {{ note[3].substring(0, 3) }}
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- note box, displays one single bookmarked note -->
    <div
      class="cluster_box"
      :id="'cluster_note_' + cluster[0].id"
      v-if="cluster[0].cluster && cluster[6]"
      style="width:100%; background-color:var(--grey-opac)"
    >
      <div style="padding:1rem;">
        <div class="display_flex" style="justify-content: space-between;">
          <div>
            <span style="font-weight: bold;"> NOTE: </span>
            <span
              v-for="(dep, ind) in cluster[0].department"
              v-bind:key="ind"
              style="font-weight: bold;"
              >{{ dep }}</span
            >
            <span style="font-weight: bold; font-size:small">
              {{ cluster[0].date_start.substring(0, 2) }}
              {{ months[parseInt(cluster[0].date_start.substring(3, 5)) - 1] }}
              {{ cluster[0].date_start.substring(6, 10) }}</span
            >
          </div>
          <div style="padding-left: 0.5rem; color:var(--dark-grey)">
            <span v-if="bookmark == false" v-on:click="bookmark_change_notes">
              <font-awesome-icon :icon="['far', 'star']" />
              <!-- far/fas star -->
            </span>
            <span v-if="bookmark == true" v-on:click="bookmark_change_notes">
              <font-awesome-icon :icon="['fas', 'star']" />
              <!-- far/fas star -->
            </span>
          </div>
        </div>

        <div>
          <div class="fixed_width inline">
            <h4>Open note:</h4>            
            <div
              v-if="search_previews[0]"
              class="tooltip"
              :id="'button_' + cluster[0].id"
            >
              <button
                v-if="search_previews[0].length > 0"
                v-on:click="open_note_alone(cluster[0].id)"
                class="button button_style button_note"
                style="margin-right: 0.5rem; background-color: #F6BE00 !important; color:var(--darkest-grey) !important; 
                                        border: 2px solid !important;"
              >
                {{ cluster[0].id + 1 }}. {{ cluster[0].title.substring(0, 3) }}
              </button>

              <div
                v-if="search_previews[0].length > 0"
                class="tooltiptext"
                :id="'snippet_' + cluster[0].id"
              >
                <p v-for="(snippet, i) in search_previews[0]" v-bind:key="i">
                  ... {{ snippet }} ...
                </p>
                <span
                  class="tooltip_arrow"
                  :id="'snippet_arrow_' + cluster[0].id"
                ></span>
              </div>

              <button
                v-if="!search_previews[0].length > 0"
                v-on:click="open_note_alone(cluster[0].id)"
                class="button button_style button_note"
                style="margin-right: 0.5rem;"
              >
                {{ cluster[0].id + 1 }}. {{ cluster[0].title.substring(0, 3) }}
              </button>
            </div>
            <div v-if="!search_previews[0]" :id="'button_' + cluster[0].id">
              <button
                v-if="!search_previews[0]"
                v-on:click="open_note_alone(cluster[0].id)"
                class="button button_style button_note"
                style="margin-right: 0.5rem;"
              >
                {{ cluster[0].id + 1 }}. {{ cluster[0].title.substring(0, 3) }}
              </button>
            </div>            
          </div>
        </div>
        <div style="margin-top:0.5rem">
          <div class="display_flex">
            <div
              style=" display: flex; justify-content: center; align-items: center;"
            >
              <div>
                Part of CLUSTER: {{ cluster_info_bookmarked_notes[1] }}
                <span
                  v-for="(dep, ind) in cluster_info_bookmarked_notes[2]"
                  v-bind:key="ind"
                  >{{ dep }},
                </span>
                <span
                  style="font-weight: bold; font-size:small"
                  v-if="
                    cluster_info_bookmarked_notes[3] !=
                      cluster_info_bookmarked_notes[4]
                  "
                >
                  {{ cluster_info_bookmarked_notes[3].substring(0, 2) }}
                  {{
                    months[
                      parseInt(
                        cluster_info_bookmarked_notes[3].substring(3, 5)
                      ) - 1
                    ]
                  }}
                  {{ cluster_info_bookmarked_notes[3].substring(6, 10) }} till
                  {{ cluster_info_bookmarked_notes[4].substring(0, 2) }}
                  {{
                    months[
                      parseInt(
                        cluster_info_bookmarked_notes[4].substring(3, 5)
                      ) - 1
                    ]
                  }}
                  {{ cluster_info_bookmarked_notes[4].substring(6, 10) }}</span
                >
                <span
                  style="font-weight: bold; font-size:small"
                  v-if="
                    cluster_info_bookmarked_notes[4] ==
                      cluster_info_bookmarked_notes[3]
                  "
                >
                  {{ cluster_info_bookmarked_notes[4].substring(0, 2) }}
                  {{
                    months[
                      parseInt(
                        cluster_info_bookmarked_notes[4].substring(3, 5)
                      ) - 1
                    ]
                  }}
                  {{ cluster_info_bookmarked_notes[4].substring(6, 10) }}
                </span>
              </div>
            </div>            
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import conceptSpace from "../assets/tagged.json";

export default {
  name: "Cluster",
  props: ["cluster"], //[cluster, [[id note, date note, text, title], [id note, date note, text, title],...], search_text, search, search_result]
  data() {
    return {
      prev_word: "", //previously clicked summary word
      same_word_count: 0, //checks if previous words is the same word as the word the user currently clicked on
      search_text: false, //display yellow marking search results
      search: "", //searched term
      search_result: "", // search result
      search_previews: [], //previews of search hits, per note in cluster > ['text text text', 'text text text']
      notes: [], // all notes belonging to this cluster [[id, date, text, snippets], ]
      search_hits: [], //summary words that match need yellow marking
      bookmark: false, //bookmark cluster
      cluster_info_bookmarked_notes: [], // if cluster > empty, if note > cluster id, title, dep, start, stop
      cluster_color: { //color background cluster box
        color: "var(--grey)",
      },
      cluster_background: {
        backgroundColor: "var(--grey)",
      },
      stripe_background: {
        backgroundColor: "var(--grey)",
      },
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
      fabians_version: false, //display either hierarchical/salient word summaries or concept space predictions (fabian's version)
      concept_space_data: {}, //data for predictions, containing main categories with percetage and sentences contributing to this prediction
    };
  },
  methods: {
    //highlight word in word summary if user clicks on it
    //word is the word(s) to be highlighted
    highlight_word(word) {
      let word_array = [];
      if (this.fabians_version) {
        word_array = word[1];
        word = word[0];
      }
      word = word.toLowerCase();
      if (this.prev_word != "") {
        let prev_pNode = document.getElementById("word_" + this.prev_word);
        prev_pNode.innerHTML = "<span> " + this.prev_word + "</span>";
      }
      let pNode = document.getElementById("word_" + word);
      if (word == this.prev_word) {
        if (this.same_word_count % 2 != 0) {
          pNode.innerHTML =
            "<span style='color:var(--red);'> " + word + "</span>";
        } else {
          pNode.innerHTML = "<span> " + word + "</span>";
        }
        this.same_word_count++;
      } else {
        pNode.innerHTML =
          "<span style='color:var(--red);'> " + word + "</span>";
        this.same_word_count = 0;
      }
      this.prev_word = word;
      if (this.fabians_version) {
        //emit to also highlight it in note text 
        this.$emit("highlight-word", [
          word_array,
          this.cluster[1][0][0],
          this.same_word_count,
        ]); //id of the first note
      } else {
        this.$emit("highlight-word", [
          word,
          this.cluster[1][0][0],
          this.same_word_count,
        ]); //id of the first note
      }
    },
    //check is search term or a synonym is a summary word in cluster, if yes > mark it yellow
    search_words(word) {
      word = word.toLowerCase();
      let pNode = document.getElementById("word_" + word);
      pNode.innerHTML =
        "<span style='background-color:var(--green);'>" + word + "</span>";
      this.search_hits.push(word);
    },
    //display search previews, word = word contained in search that is present in a note, id = id of that note
    previews(word, id) {
      word = word.toLowerCase();
      console.log(word);
      let note_text_org = this.notes[id][2];
      let note_text = note_text_org;
      note_text = note_text.replace(/(\r\n|\n|\r)/gm, "");
      //searched terms contains spaces
      if (word.split(" ").length > 1) {
        let word_split = word.split(" ");
        let new_word = "";
        for (let j = 0; j < word_split.length; j++) {
          if (j == 0) {
            new_word += word_split[j];
          } else {
            new_word += "A" + word_split[j];
          }
        }

        note_text = note_text.toLowerCase();
        note_text = note_text.replace(word, new_word);
        note_text = note_text
          .replace(/[^\w\s]|_/g, function($1) {
            return " " + $1 + " ";
          })
          .replace(/[ ]+/g, " ")
          .split(" ");
        word = new_word;
      } else {
        note_text = note_text.toLowerCase();
        //split on punctuation and whitespaces
        note_text = note_text
          .replace(/[^\w\s]|_/g, function($1) {
            return " " + $1 + " ";
          })
          .replace(/[ ]+/g, " ")
          .split(" ");
      }
      if (this.cluster[0].id == 46) {
        console.log(note_text);
      }
      //if searched term does not contain spaces
      if (note_text.includes(word)) {
        console.log("in include loop");
        let ind_word = this.getAllIndexes(word, note_text);
        for (let j = 0; j < ind_word.length; j++) {
          let string_snippet = "";
          let start = ind_word[j] - 5;
          let stop = ind_word[j] + 7;
          if (start < 0) {
            start = 0;
          }
          if (stop > note_text.length - 1) {
            stop = note_text.length - 1;
          }
          let tmp = note_text.slice(start, stop);
          for (let k = 0; k < tmp.length; k++) {
            string_snippet += tmp[k] + " ";
          }
          if (string_snippet.includes("A")) {
            string_snippet = string_snippet.replace("A", " ");
          }
          this.search_previews[id].push(string_snippet);
        }
        setTimeout(() => this.snippet_display(this.cluster[1][id][0]), 100);
      }
      console.log("snippets");
      console.log(this.cluster[0].id);
      console.log(this.search_previews);
    },
    //get all indexes of notes that contain a certain string
    //searchStr = string to search for, str= note text
    getAllIndexes(searchStr, str) {
      var searchStrLen = searchStr.length;
      if (searchStrLen == 0) {
        return [];
      }
      var startIndex = 0,
        index,
        indices = [];
      while ((index = str.indexOf(searchStr, startIndex)) > -1) {
        indices.push(index);
        startIndex = index + searchStrLen;
      }
      return indices;
    },
    //change in a cluster bookmark
    bookmark_change() {
      this.bookmark = !this.bookmark;
      let data = [this.cluster[0].id, this.bookmark];
      this.$emit("cluster-bookmark", data);
    },
    //change in a note cluster bookmark
    bookmark_change_notes() {
      this.bookmark = !this.bookmark;
      let data = [this.cluster[0].id, this.bookmark];
      this.$emit("note-bookmark", data);
    },
    //open notes from this cluster on the side, and scroll automatically to 'note' 
    open_note(note) {
      this.$emit("open-note", note);
    },
    //open note in note box
    open_note_alone(note) {
      this.$emit("open-note-alone", note);
    },
    //display snippets of note where id is 'id'
    snippet_display(id) {
      if (document.getElementById("cluster_" + this.cluster[0].id)) {
        let element = document.getElementById("button_" + id);
        let element_offset = element.offsetLeft;
        let cluster_offset = document.getElementById(
          "cluster_" + this.cluster[0].id
        ).offsetLeft;
        let width =
          "calc(" +
          String(
            document.getElementById("cluster_" + this.cluster[0].id).clientWidth
          ) +
          "px - 2rem )";
        if (document.getElementById("snippet_" + id)) {
          let margin_left =
            "calc(" +
            String(-1 * (element_offset - cluster_offset)) +
            "px + 1rem )";
          document.getElementById(
            "snippet_" + id
          ).style.marginLeft = margin_left;
          document.getElementById("snippet_" + id).style.width = width;
          document.getElementById("snippet_arrow_" + id).style.marginLeft =
            String(element_offset - cluster_offset + 20) + "px";
        }
      }
    },
  },
  watch: {
    cluster() {
      console.log("cluster");
      console.log(this.cluster);
      this.notes = this.cluster[1];
      this.bookmark = this.cluster[0].bookmark;
      //make preview snippets empty array length of amount of notes
      this.search_previews = [];
      for (let i = 0; i < this.notes.length; i++) {
        this.search_previews.push([]);
      }
      //if a search is executed 
      if (this.cluster[2] == true && this.cluster[4] != "no results") {
        this.search_text = this.cluster[2];
        this.search = this.cluster[3];
        this.search_result = this.cluster[4];
        this.search_result = this.search_result.map((term) =>
          term.toLowerCase()
        );
        if (this.search_text == true && !this.cluster[0].text) {
          //check if it is not a note cluster
          for (let i = 0; i < this.cluster[0].procedure_words.length; i++) {
            if (
              this.cluster[0].procedure_words[i].toLowerCase() ==
              this.search.toLowerCase()
            ) {
              this.search_words(this.cluster[0].procedure_words[i]);
            }
            if (this.search_result.includes(this.search.toLowerCase())) {
              let tmp = this.search_result.indexOf(this.search.toLowerCase());
              this.search_words(this.search_result[tmp]);
            }
          }
          for (let i = 0; i < this.cluster[0].disease_words.length; i++) {
            if (
              this.cluster[0].disease_words[i].toLowerCase() ==
              this.search.toLowerCase()
            ) {
              this.search_words(this.cluster[0].disease_words[i]);
            }
            if (this.search_result.includes(this.search.toLowerCase())) {
              let tmp = this.search_result.indexOf(this.search.toLowerCase());
              this.search_words(this.search_result[tmp]);
            }
          }
          for (let i = 0; i < this.cluster[0].drugs_words.length; i++) {
            if (
              this.cluster[0].drugs_words[i].toLowerCase() ==
              this.search.toLowerCase()
            ) {
              this.search_words(this.cluster[0].drugs_words[i]);
            }
            if (this.search_result.includes(this.search.toLowerCase())) {
              let tmp = this.search_result.indexOf(this.search.toLowerCase());
              this.search_words(this.search_result[tmp]);
            }
          }
        }
        //preview snippets
        if (this.cluster[0].text) {
          let note = this.cluster[0].text; //get the text of the note
          note = note.toLowerCase();
          if (note.includes(this.search.toLowerCase())) {
            console.log("previews1");
            console.log(this.cluster[0].id);
            setTimeout(() => this.previews(this.search, 0), 100);
          }
          //for all synonyms in the search
          for (let j = 0; j < this.search_result.length; j++) {
            if (note.includes(this.search_result[j])) {
              setTimeout(() => this.previews(this.search_result[j], 0), 100);
            }
          }
        } else {
          for (let i = 0; i < this.cluster[1].length; i++) {
            let note = this.cluster[1][i][2]; //get the text of the note
            note = note.toLowerCase();
            if (note.includes(this.search.toLowerCase())) {
              console.log("previews1");
              console.log(this.cluster[0].id);
              setTimeout(() => this.previews(this.search, i), 100);
            }
            //for all synonyms in the search
            for (let j = 0; j < this.search_result.length; j++) {
              if (note.includes(this.search_result[j])) {
                setTimeout(() => this.previews(this.search_result[j], i), 100);
              }
            }
          }
        }

      } else if (this.cluster[2] == false || this.cluster[4] == "no results") { //no search executed
        this.search_text = false;
        if (this.search != "" && this.search_hits) { //reset yellow markings
          for (let i = 0; i < this.search_hits.length; i++) {
            document.getElementById(
              "word_" + this.search_hits[i]
            ).innerHTML = this.search_hits[i];
          }
          this.search_hits = [];
        }
      }
    
      if (this.cluster[6]) {
        this.cluster_info_bookmarked_notes = this.cluster[6];
      }

    },
  },
  created() {
    console.log("cluster");
    console.log(this.cluster);
    this.bookmark = this.cluster[0].bookmark;
    if (this.cluster[6]) {
      this.cluster_info_bookmarked_notes = this.cluster[6];
    }

    if (this.cluster[0].name) {
      //then this is a cluster summary box
      if (this.cluster[0].name.includes("check_up")) {
        this.cluster_color.color = "var(--blue)";
        this.cluster_background.backgroundColor = "var(--blue-opac)";
        this.stripe_background.backgroundColor = "var(--blue)";
      } else if (this.cluster[0].name.includes("admis")) {
        this.cluster_color.color = "var(--orange)";
        this.cluster_background.backgroundColor = "var(--orange-opac)";
        this.stripe_background.backgroundColor = "var(--orange)";
      }
    }
    if (this.cluster[0].cluster) {
      //then this is a note box
      if (this.cluster[0].cluster.includes("check_up")) {
        this.cluster_color.color = "var(--blue)";
        this.cluster_background.backgroundColor = "var(--blue-opac)";
      } else if (this.cluster[0].cluster.includes("admis")) {
        this.cluster_color.color = "var(--orange)";
        this.cluster_background.backgroundColor = "var(--orange-opac)";
      }
    }

    //concept spaces
    if (this.cluster[0].name) {
      //then this is a cluster in the box
      this.concept_space_data = conceptSpace[this.cluster[0].name];
    }
  },
};
</script>

<style scoped>
.cluster_box {
  margin: 0.5rem 0;
}

.inline {
  display: inline-block;
  vertical-align: top;
}

.fixed_width {
  width: 160px;
}

.link {
  color: var(--lightest-grey);
  text-decoration: none;
}

.link:hover {
  color: var(--lightest-grey);
  text-decoration: none;
  cursor: pointer;
}

.tooltip {
  position: relative;
}

.tooltiptext {
  visibility: hidden;
  width: 300%;
  background-color: var(--darkest-grey);
  color: var(--lightest-grey);
  border-radius: 6px;
  padding: 0.5rem;
  position: absolute;
  z-index: 2;
}

.tooltip_arrow {
  content: "";
  position: absolute;
  margin-left: -5px;
  border-width: 5px;
  bottom: 100%;
  border-style: solid;
  border-color: transparent transparent var(--darkest-grey) transparent;
}

.tooltip:hover .tooltiptext {
  visibility: visible;
}
</style>
