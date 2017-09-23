/**
 * Created by peter on 04.03.17.
 */
import React, {Component} from 'react';
import Title from './Title'
import { Link } from 'react-router'
import {Col, Row, Panel} from 'react-bootstrap';
import PieChart from './PieChart';
import picPlaceholder from '../public/Portrait_placeholder.png'

class MemberPage extends Component {

    state = {
        content: 'MEMBER',
        member: {
            photos: []
        },
        twitter: null,
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
        const url = 'https://botornot-hessen-api.herokuapp.com/pbc/users/' + this.props.params.slug;
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
        const followerCount = <Col sm={12} xs={6}>
            Gesamt: <span className="number">{this.state.followers.numFollowers}</span><br />
            Bots: <span className="number">{this.state.followers.numBots}</span><br />
            Menschen: <span className="number">{this.state.followers.numHumans}</span></Col>;
        const retweetCount = this.state.retweets.numHumans + this.state.retweets.numBots;
        const retweetersCount = this.state.retweeters.numHumans + this.state.retweeters.numBots;
        return (
          <div className="container">
            <Title />
              <div><Link to="/" className="btn btn-default">« Zurück</Link></div>
              <img className="Profile-picture" alt="Profilbild"
                  src={getPhoto(this.state.member.photos, this.state.twitter)}/>
              <Panel bsStyle="primary" className="App-profile" bsSize="large">
                  <p>Name: {this.state.member.name ? this.state.member.name : '-'}</p>
                  <p>Partei: {this.state.member.party ? this.state.member.party : '-'}</p>
                  <p>Twitter-Account: {this.state.member.twitter_handle ? getTwitterLink(this.state.member.twitter_handle) : '-'}</p>
              </Panel>

            <Row className="App-info">
                <Col sm={4}>
                  <div>
                      <h4>Follower</h4>
                      <Row>
                          <Col sm={12} xs={6}><PieChart className="Info-followers" numbers={this.state.followers}/></Col>
                          {followerCount}
                      </Row>
                  </div>
                </Col>
                <Col xs={6} sm={4}>
                    <div>
                      <h4>Retweets</h4>
                      <PieChart className="Info-retweets" numbers={this.state.retweets}/>
                        <em>Daten folgen in den nächsten Tagen</em>
                    </div>
                </Col>
                <Col xs={6} sm={4}>
                    <div>
                      <h4>Retweeters</h4>
                      <PieChart className="Info-retweeters" numbers={this.state.retweeters}/>
                        <em>Daten folgen in den nächsten Tagen</em>
                    </div>
                </Col>
            </Row>
          </div>
        )
    }
}

function getPhoto(photos, twitter) {
    if (photos.length === 0) {
        return (twitter && twitter.profile_url.replace('_normal', '')) || picPlaceholder;
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
