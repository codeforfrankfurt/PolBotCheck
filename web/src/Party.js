/**
 * Created by peter on 04.03.17.
 */
import React, {Component} from 'react';

export default class PartyPage extends Component {
  state = {
    member: {
      name: "max meister",
      pictureURL: "http://www.billboard.com/files/styles/article_main_image/public/media/donald-trump-thumbs-up-aug-2015-billboard-650.jpg",
      party: "Die Linke",
      followers: {
        numFollowers: 3141592653,
        ratioBots: "22%"
      },
      retweets: {
        numRetweets: 1248653,
        ratioBots: "47%"
      },
      wordCluster: {
        hashTags: [
          "#fakeNews",
          "#letsBuildAWall"
        ],
        topics: [
          "immigration",
          "freeSpeech"
        ]
      }
    }
  };

  render() {
    return (
      <div>
         </div>
    )
  }
}