import React from 'react';
import AvatarFrame from './AvatarFrame';

/**
 * CommitteeMembers - Responsive grid of committee member cards
 *
 * @param {Array} members - Array of { name, designation, photo } objects
 */
const CommitteeMembers = ({ members = [] }) => {
  return (
    <section className="py-12 px-4 bg-[#F4F7F5]">
      <div className="max-w-6xl mx-auto">
        {/* Section Header */}
        <div className="text-center mb-12">
          <span className="inline-block text-sm font-semibold uppercase tracking-[3px] text-[#0A5C36] bg-[#0A5C36]/10 px-4 py-1.5 rounded-full mb-3">
            Our Leadership
          </span>
          <h2 className="text-3xl md:text-4xl font-bold text-slate-800 mb-3">
            Committee Members
          </h2>
          <div className="w-16 h-1 bg-gradient-to-r from-[#0A5C36] to-[#12A374] mx-auto rounded-full" />
        </div>

        {/* Responsive Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {members.map((member, index) => (
            <AvatarFrame
              key={member.id || index}
              name={member.name}
              designation={member.designation}
              photo={member.photo}
            />
          ))}
        </div>

        {members.length === 0 && (
          <p className="text-center text-gray-500 py-12">No committee members found.</p>
        )}
      </div>
    </section>
  );
};

export default CommitteeMembers;
