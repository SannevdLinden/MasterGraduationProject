<template>
  <div class="scroll height_95" id="notes_container">
    <div v-if="notes_id_display[0][1]">
      <!-- display the note titles, text and attached quant data button if there is data-->
      <div
        v-for="(note, index) in notes_id_display[0][1].slice().reverse()"
        v-bind:key="note.id"
        :id="note.id"
        style="padding-right:1rem; margin-top:1rem;"
      >
        <div class="display_flex" style="justify-content: space-between;">
          <div>
            <h3 style="font-weight:bold">
              NOTE {{ note.id + 1 }}: {{ note.title }}
              <span style="font-size:small"
                >{{ note.date_start.substring(0, 2) }}
                {{ months[parseInt(note.date_start.substring(3, 5)) - 1] }}
                {{ note.date_start.substring(6, 10) }}
              </span>
            </h3>
          </div>
          <div>
            <span
              v-if="
                bookmark_notes[notes_id_display[0][1].length - 1 - index] ==
                  false
              "
              v-on:click="
                bookmark_change(notes_id_display[0][1].length - 1 - index)
              "
            >
              <font-awesome-icon :icon="['far', 'star']" />
              <!-- far/fas star -->
            </span>
            <span
              v-if="
                bookmark_notes[notes_id_display[0][1].length - 1 - index] ==
                  true
              "
              v-on:click="
                bookmark_change(notes_id_display[0][1].length - 1 - index)
              "
            >
              <font-awesome-icon :icon="['fas', 'star']" />
              <!-- far/fas star -->
            </span>
          </div>
        </div>
        <br />
        <p :id="'note_text' + note.id" v-html="note.text"></p>
        <div v-if="quant_data_buttons[index] == true">
          <button
            class="button button_style"
            v-on:click="$emit('full-screen', note.id)"
          >
            Attached quantitative data
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import quant_data from "../assets/chartevents.json";

export default {
  name: "NotesList",
  props: ["notes_id_display"], //notes to display
  data() {
    return {
      search_text: false, //if the yellow marking of matches to the search should be displayed
      search: "", //searched terms
      search_result: "", //search synonyms 
      search_executed: false, //if search was done
      prev_highlight_word: "", //previous summary word the user clicked on to highlight 
      prev_highlight_word_fab: [], //previous concept space concept the user clicked on to highlight 
      bookmark_notes: [], //bookmarks of all the notes
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
      fabians_version: false, //display concept space highlight or hierarchical/salient word summaries highlight
      quant_data_buttons: [], //per note is there is quant data available 
      quant_data: new Set(), //set with all days there is quant data available
    };
  },
  methods: {
    //highlight words in text in color from the search actions or the action where the user clicked on a summary word
    //if highlighted word comes from a search action
    highlight_word(word, color, search) {
      console.log("high");
      console.log(word);
      //reset highlight
      if (word == "") {
        for (let i = 0; i < this.notes_id_display[0][1].length; i++) {
          let id = this.notes_id_display[0][1][i].id;
          let text = document.getElementById("note_text" + id).innerHTML;
          if (!search) {
            //clear the previous span
            text = text.replace(/style="color:red"/g, "");
          }
          document.getElementById("note_text" + id).innerHTML = text;
        }
      } else {
        if (this.fabians_version) {
          for (let i = 0; i < word.length; i++) {
            word[i] = word[i].toLowerCase();
          }
        } else {
          word = word.toLowerCase();
        }
        for (let i = 0; i < this.notes_id_display[0][1].length; i++) {
          let id = this.notes_id_display[0][1][i].id;
          let text = document.getElementById("note_text" + id).innerHTML;
          if (!search) {
            //clear the previous span
            text = text.replace(/style="color:red"/g, "");
            document.getElementById("note_text" + id).innerHTML = text;
          }
          if (!this.fabians_version) {
            let final_text = "";
            let char_counter = 0;
            let text_array = text.toLowerCase();
            text_array = text_array.split(word);
            //mark all occurences of the to be highlighted word by injecting colors spans around the word(s)
            for (let j = 0; j < text_array.length; j++) {
              if (j == text_array.length - 1) {
                // last part of the text
                if (text_array.length > 1) {
                  //text need to go till the end of the string
                  if (search) {
                    final_text +=
                      "<span style='background-color:var(--" +
                      color +
                      ")'>" +
                      text.substring(char_counter, char_counter + word.length) +
                      "</span>";
                  } else if (this.prev_highlight_word != word) {
                    final_text +=
                      "<span style='color:" +
                      color +
                      "'>" +
                      text.substring(char_counter, char_counter + word.length) +
                      "</span>";
                  }
                  char_counter += word.length;
                  final_text += text.substring(char_counter, text.length);
                } else {
                  //if the word does not occur return original text
                  final_text = text;
                }
              } else {
                if (j != 0) {
                  if (search) {
                    final_text +=
                      "<span style='background-color:var(--" +
                      color +
                      ")'>" +
                      text.substring(char_counter, char_counter + word.length) +
                      "</span>";
                  } else if (this.prev_highlight_word != word) {
                    final_text +=
                      "<span style='color:" +
                      color +
                      "'>" +
                      text.substring(char_counter, char_counter + word.length) +
                      "</span>";
                  }
                  char_counter += word.length;
                }
                final_text += text.substring(
                  char_counter,
                  char_counter + text_array[j].length
                );
                char_counter += text_array[j].length;
              }
            }

            document.getElementById("note_text" + id).innerHTML = final_text;
          } else {
            //highlight all the sentences that contributed to the prediction of concept by injecting colored spans
            for (let k = 0; k < word.length; k++) {
              text = document.getElementById("note_text" + id).innerHTML;
              let final_text = "";
              let char_counter = 0;
              let text_array = text.toLowerCase();
              text_array = text_array.split(word[k]);

              for (let j = 0; j < text_array.length; j++) {
                if (j == text_array.length - 1) {
                  // last part of the text
                  if (text_array.length > 1) {
                    //text need to go till the end of the string
                    if (search) {
                      final_text +=
                        "<span style='background-color:var(--" +
                        color +
                        ")'>" +
                        text.substring(
                          char_counter,
                          char_counter + word[k].length
                        ) +
                        "</span>";
                    } else if (this.prev_highlight_word_fab != word) {
                      final_text +=
                        "<span style='color:" +
                        color +
                        "'>" +
                        text.substring(
                          char_counter,
                          char_counter + word[k].length
                        ) +
                        "</span>";
                    }
                    char_counter += word[k].length;
                    final_text += text.substring(char_counter, text.length);
                  } else {
                    //if the word does not occur return original text
                    final_text = text;
                  }
                } else {
                  if (j != 0) {
                    if (search) {
                      final_text +=
                        "<span style='background-color:var(--" +
                        color +
                        ")'>" +
                        text.substring(
                          char_counter,
                          char_counter + word[k].length
                        ) +
                        "</span>";
                    } else if (this.prev_highlight_word_fab != word) {
                      final_text +=
                        "<span style='color:" +
                        color +
                        "'>" +
                        text.substring(
                          char_counter,
                          char_counter + word[k].length
                        ) +
                        "</span>";
                    }
                    char_counter += word[k].length;
                  }
                  final_text += text.substring(
                    char_counter,
                    char_counter + text_array[j].length
                  );
                  char_counter += text_array[j].length;
                }
              }

              document.getElementById("note_text" + id).innerHTML = final_text;
            }
          }
        }
      }
    },
    //reset all highlighting related to a search action
    reset() {
      for (let i = 0; i < this.notes_id_display[0][1].length; i++) {
        let id = this.notes_id_display[0][1][i].id;
        let text = document.getElementById("note_text" + id).innerHTML;
        document.getElementById("note_text" + id).innerHTML = text.replaceAll(
          'style="background-color:var(--green)"',
          ""
        );
      }
    },
    //bookmark of a note changes where index = 'index' in note array
    bookmark_change(index) {
      this.bookmark_notes[index] = !this.bookmark_notes[index];
      console.log(this.bookmark_notes);
      let data = [
        this.notes_id_display[0][1][index].id,
        this.bookmark_notes[index],
      ];
      this.$emit("notes-bookmark", data);
    },
  },
  watch: {
    notes_id_display() {
      //user clicked on other word/concept in word summary      
      if (this.notes_id_display[0][2] || this.notes_id_display[0][2] == "") {
        setTimeout(
          () => this.highlight_word(this.notes_id_display[0][2], "red", false),
          100
        );
      }

      //fill bookmark_notes with all bookmarks
      this.bookmark_notes = [];
      if (this.notes_id_display[0][1]) {
        for (let i = 0; i < this.notes_id_display[0][1].length; i++) {
          this.bookmark_notes.push(this.notes_id_display[0][1][i].bookmark);
        }
      }

      //scroll to note corresponding to the button the user clicked
      const elmnt = document.getElementById(
        String(this.notes_id_display[0][0])
      );
      if (elmnt) {
        setTimeout(() => elmnt.scrollIntoView(), 100);
      }
      this.$emit("notes-loaded");

      //if search is executed
      if (
        this.notes_id_display[1] == true &&
        this.notes_id_display[0][1] &&
        this.notes_id_display[3] != "no results"
      ) {
        
        this.search_text = this.notes_id_display[1];
        this.search = this.notes_id_display[2];
        this.search_result = this.notes_id_display[3];
        this.search_result = this.search_result.map((term) =>
          term.toLowerCase()
        );

        for (let i = 0; i < this.notes_id_display[0][1].length; i++) {
          let note = this.notes_id_display[0][1][i].text;
          note = note.toLowerCase();
          if (note.includes(this.search.toLowerCase())) {
            setTimeout(
              () => this.highlight_word(this.search, "green", true),
              100
            );
          }
          for (let j = 0; j < this.search_result.length; j++) {
            if (note.includes(this.search_result[j])) {
              setTimeout(
                () => this.highlight_word(this.search_result[j], "green", true),
                100
              );
            }
          }
        }
        
      }
      //reset search
      if (
        (this.notes_id_display[3] == "no results" ||
          this.notes_id_display[2] == "") &&
        this.notes_id_display[0][1]
      ) {
        this.search = "";
        setTimeout(() => this.reset(), 100);
      }
      //check which notes have attached quantiative data
      console.log('quant data buttons');
      console.log(this.quant_data);
      if (this.notes_id_display[0][1]) {
        for (let i = 0; i < this.notes_id_display[0][1].length; i++) {
          if (this.quant_data.has(this.notes_id_display[0][1][i].date_start)) {
            this.quant_data_buttons.push(true);
          } else {
            this.quant_data_buttons.push(false);
          }
        }
        this.quant_data_buttons = this.quant_data_buttons.slice().reverse();
      }
    },
  },
  created() {
    this.bookmark_notes = [];
    if (this.notes_id_display[0][1]) {
      for (let i = 0; i < this.notes_id_display[0][1].length; i++) {
        this.bookmark_notes.push(this.notes_id_display[0][1][i].bookmark);
      }

      //change scrolling to id of note where bookmark changed
      const elmnt = document.getElementById(
        String(this.notes_id_display[0][0])
      );
      if (elmnt) {
        elmnt.scrollIntoView();
      }
    }

    //change date format quant data to format date of notes
    for (let i = 0; i < quant_data.length; i++) {
      let day = quant_data[i].date.replaceAll("/", "-");
      day = day.substring(0, 10);
      this.quant_data.add(day);
    }
    
  },
};
</script>

<style scoped>
.height_95 {
  height: 83vh;
}
</style>
