import React from 'react';
import PropTypes from 'prop-types';

import ArtifactsList from '../components/ArtifactsList';
import AsyncPage from '../components/AsyncPage';
import Section from '../components/Section';

export default class BuildArtifacts extends AsyncPage {
  static contextTypes = {
    ...AsyncPage.contextTypes,
    build: PropTypes.object.isRequired,
    repo: PropTypes.object.isRequired
  };

  getEndpoints() {
    let {repo} = this.context;
    let {buildNumber} = this.props.params;
    return [['artifacts', `/repos/${repo.full_name}/builds/${buildNumber}/artifacts`]];
  }

  renderBody() {
    return (
      <Section>
        {this.state.artifacts.length
          ? <ArtifactsList artifacts={this.state.artifacts} />
          : <em>This build did not produce artifacts.</em>}
      </Section>
    );
  }
}
