/**
 * Created by peter on 04.03.17.
 */
import React, {Component} from 'react';
import Title from './Title'
import { Link } from 'react-router'
import {Col, Row, Panel} from 'react-bootstrap';
import PieChart from './PieChart';
import BarChart from './BarChart';
import picPlaceholder from '../public/Portrait_placeholder.png'

class MemberPage extends Component {

    state = {
        content: 'MEMBER',
        member: {
            photos: []
        },
        followers: {
            numFollowers: null,
            numHumans: null,
            numBots: null
        },
        retweets: {
            numRetweets: null,
            numHumans: null,
            numBots: null
        },
        retweeters: {
            numRetweeters: null,
            numHumans: null,
            numBots: null
        },
        wordCluster: {
            topics: []
        }
    };

    componentWillMount() {
        let self = this;
        const url = 'https://botornot-hessen-api.herokuapp.com/pbc/user/' + this.props.params.slug;
        fetch(url, {mode: 'cors', headers: {'Accept': 'application/json'}})
            .then(res => {
                return res.json().then(data => {
                    self.state = data;
                    console.log(data);

                    // deactivate retweets and & retweeters for now.
                    Object.assign(self.state, {
                        retweets: {
                            numRetweets: null,
                            numHumans: null,
                            numBots: null
                        },
                        retweeters: {
                            numRetweeters: null,
                            numHumans: null,
                            numBots: null
                        }
                    });

                    self.setState(self.state);
                });
            })
            .catch(e => console.log("error fetching " + url, e));
    }

    render() {
        const followerCount = <span>Gesamt: {this.state.followers.numFollowers}, analysierte<br />
            Bots: {this.state.followers.numBots} oder Menschen: {this.state.followers.numHumans}</span>;
        const retweetCount = this.state.retweets.numHumans + this.state.retweets.numBots;
        const retweetersCount = this.state.retweeters.numHumans + this.state.retweeters.numBots;
        return (
          <div className="container">
            <Title />
              <div><Link to="/">Zurück</Link></div>
            <Row className="App-profile" >
                <Col md={4}>
                  <img className="Profile-picture" alt="Profilbild"
                       src={getPhoto(this.state.member.photos)}/>
                </Col>
                <Col md={4}>
                  <Panel bsStyle="primary"
                         bsSize="large">
                    <p>Name: {this.state.member.name ? this.state.member.name : '-'}</p>
                    <p>Partei: {this.state.member.party ? this.state.member.party : '-'}</p>
                    <p>Twitter-Account: {this.state.member.twitter_handle ? getTwitterLink(this.state.member.twitter_handle) : '-'}</p>
                  </Panel>
                </Col>
            </Row>
            <Row>
                <Col className="App-info" md={12}>
                  <Row>
                    <Col md={4}>
                      <h4>Follower ({followerCount})</h4>
                      <PieChart className="Info-followers" numbers={this.state.followers}/>
                    </Col>
                    <Col md={4}>
                      <h4>Retweets (<em>in den nächsten Tagen</em>)</h4>
                      <PieChart className="Info-retweets" numbers={this.state.retweets}/>
                    </Col>
                    <Col md={4}>
                      <h4>Retweeters (<em>in den nächsten Tagen</em>)</h4>
                      <PieChart className="Info-retweeters" numbers={this.state.retweeters}/>
                    </Col>
                  </Row>
                </Col>
            </Row>
          </div>
        )
    }
}

function getPhoto(photos) {
    if (photos.length === 0) {
        return picPlaceholder;
    } else {
        let wikimediaPhoto = photos.find((p) => p.url.indexOf('wikimedia') !== -1);
        wikimediaPhoto = wikimediaPhoto && wikimediaPhoto.url;

        let abgwPhoto = photos.find((p) => p.url.indexOf('abgeordnetenwatch') !== -1);
        if (abgwPhoto) {
            // get non-404 images through web.archive.org, the 20 is the first part of the date,
            // id_ gives the original scraped file without header
            abgwPhoto = 'https://web.archive.org/web/20id_/' + abgwPhoto.url;
        }

        if (!wikimediaPhoto && !abgwPhoto) {
            return photos[0].url;
        }

        return wikimediaPhoto ? wikimediaPhoto : abgwPhoto;
    }
}

function getTwitterLink(twitterHandle) {
    return <a href={'https://twitter.com/' + twitterHandle}>{twitterHandle}</a>;
}

export default MemberPage;
